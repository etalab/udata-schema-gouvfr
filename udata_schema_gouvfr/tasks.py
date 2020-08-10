import re
import csv
import codecs
import logging

import requests

from udata.tasks import job
from udata.core.dataset.models import get_resource, ResourceSchema

log = logging.getLogger(__name__)


IRVE_STABLE_DATASET_URL = (
    "https://www.data.gouv.fr/fr/datasets/r/50625621-18bd-43cb-8fde-6b8c24bdabb3"
)
IRVE_SCHEMA = "etalab/schema-irve"


def find_sources():
    """
    Find all (dataset, resource) listed in the consolidated IRVE resource
    """
    response = requests.get(IRVE_STABLE_DATASET_URL)
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
        resource = get_resource(resource_id)
        if not resource:
            raise ValueError(f'Cannot find a resource with ID {resource_id}')
        resource.schema = IRVE_SCHEMA
        resource.save()
        log.info(f'Set the {IRVE_SCHEMA} on resource {resource_id} from dataset {dataset_slug}')


@job("set-irve-schemas")
def run_set_irve_schemas(self):
    set_irve_schemas(find_sources())
