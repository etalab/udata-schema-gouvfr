from flask import Blueprint

from udata import theme

from udata.frontend import template_hook

blueprint = Blueprint('schema', __name__, template_folder='templates')


def has_schema(ctx):
    resource = ctx['resource']
    return resource.schema is not None


@template_hook('dataset.resource.card.extra-buttons', when=has_schema)
def resource_schema_details(ctx):
    resource = ctx['resource']

    validation_url = f"https://validata.etalab.studio/table-schema?input=url&schema_name=schema-datagouvfr.{resource.schema}&url={resource.url}"
    documentation_url = f"https://schema.data.gouv.fr/{resource.schema}/latest.html"

    return theme.render(
        'schema-details.html',
        resource=resource,
        id=str(resource.id).replace('-', ''),
        validation_url=validation_url,
        documentation_url=documentation_url,
    )
