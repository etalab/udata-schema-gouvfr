import re
import csv
import uuid
import codecs
import logging

import requests

from flask import current_app
from udata.tasks import job
from udata.core.dataset.models import get_resource, ResourceSchema

log = logging.getLogger(__name__)


IRVE_SCHEMA = "etalab/schema-irve"


def find_sources():
    """
    Find all (dataset, resource) listed in the consolidated IRVE resource
    """
    response = requests.get(current_app.config.get('SCHEMA_GOUVFR_IRVE_STABLE_RESOURCE_URL'))
    response.raise_for_status()

    sources = set()
    reader = csv.DictReader(
        codecs.iterdecode(response.iter_lines(), "utf-8"), delimiter=";"
    )
    for record in reader:
        sources.add(record["source"])

    return sources


def ensure_irve_schema_exists():
    """
    Ensure that the IRVE schema exists
    """
    if not any([el["id"] == IRVE_SCHEMA for el in ResourceSchema.objects()]):
        raise ValueError(f"{IRVE_SCHEMA} is not a valid schema")


def set_irve_schemas(sources):
    """
    Update a list of resources by setting the schema attribute to
    the IRVE schema
    """
    ensure_irve_schema_exists()

    pattern = re.compile(
        r"^https://www\.data\.gouv\.fr/fr/datasets/([\S]+)/#resource-([\S]+)$"
    )

    log.info(f'Preparing to set the {IRVE_SCHEMA} schema on {len(sources)} resources')
    for source in sources:
        dataset_slug, resource_id = re.match(pattern, source).groups()
        resource = get_resource(uuid.UUID(resource_id))
        if not resource:
            log.warning(f'Cannot find a resource with ID {resource_id}. It may have been deleted.')
            continue
        resource.schema = IRVE_SCHEMA
        resource.save()
        log.info(f'Set the {IRVE_SCHEMA} on resource {resource_id} from dataset {dataset_slug}')


@job("set-irve-schemas")
def run_set_irve_schemas(self):
    set_irve_schemas(find_sources())
