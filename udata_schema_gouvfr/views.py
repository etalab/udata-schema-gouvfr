from urllib.parse import urlencode

from flask import Blueprint, current_app

from udata import theme
from udata.frontend import template_hook

blueprint = Blueprint('schema', __name__, template_folder='templates')


def validata_url(resource):
    base = current_app.config.get('SCHEMA_GOUVFR_VALIDATA_URL')

    query = urlencode({
        "input": "url",
        "schema_name": f"schema-datagouvfr.{resource.schema}",
        "url": resource.url,
    })

    return f"{base}/table-schema?{query}"


def resource_has_schema(ctx):
    return ctx.get('resource') and ctx['resource'].schema


def dataset_has_schema(ctx):
    if ctx.get('dataset') is None:
        return False
    return any([r.schema is not None for r in ctx['dataset'].resources])


@template_hook('dataset.resource.card.extra-buttons', when=resource_has_schema)
def resource_schema_details(ctx):
    resource = ctx['resource']

    return theme.render(
        'button.html',
        resource=resource,
        id=str(resource.id).replace('-', ''),
    )


@template_hook('base.modals', when=dataset_has_schema)
def resource_schema_modal(ctx):
    dataset = ctx['dataset']

    documentation_urls = {}
    validation_urls = {}
    for resource in [r for r in dataset.resources if r.schema]:
        validation_urls[resource.id] = validata_url(resource)
        documentation_urls[resource.id] = (
            f"https://schema.data.gouv.fr/{resource.schema}/latest.html"
        )

    return theme.render(
        'modal.html',
        dataset=dataset,
        documentation_urls=documentation_urls,
        validation_urls=validation_urls,
    )
