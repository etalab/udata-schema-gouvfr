from urllib.parse import urlencode

from flask import Blueprint, current_app

from udata import theme
from udata.frontend import template_hook

import requests

blueprint = Blueprint('schema', __name__, template_folder='templates')


def validata_url(resource,schema_url=None):
    base = current_app.config.get('SCHEMA_GOUVFR_VALIDATA_URL')
    if(schema_url):
        query = urlencode({
            "input": "url",
            "schema_url": schema_url,
            "url": resource.url,
        })
    else:
        query = urlencode({
            "input": "url",
            "schema_name": f"schema-datagouvfr.{resource.schema['name']}",
            "url": resource.url,
        })

    return f"{base}/table-schema?{query}"

def isTableSchema(schemas,current_schema):
    try:
        for schema in schemas:
            if((schema['name'] == current_schema) & (schema['schema_type'] == 'tableschema')): return True
        return False
    except:
        return False

def getSchemaUrl(schemas,current_schema,current_schema_version):
    try:
        for schema in schemas:
            if(schema['name'] == current_schema): 
                for version in schema['versions']:
                    if(version['version_name'] == current_schema_version): return version['schema_url']
        return
    except:
        return

def loadCatalog(): 
    r = requests.get(current_app.config.get('SCHEMA_CATALOG_URL'))
    try:
        return r.json()['schemas']
    except:
        return

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
    schemas = loadCatalog()

    documentation_urls = {}
    authorize_validation = {}
    validation_urls = {}
    for resource in [r for r in dataset.resources if r.schema]:

        authorize_validation[resource.id] = isTableSchema(schemas,resource.schema['name'])

        if(authorize_validation[resource.id]):
            schema_url = None
            if("version" in resource.schema):
                schema_url = getSchemaUrl(schemas,resource.schema['name'],resource.schema['version'])
            validation_urls[resource.id] = validata_url(resource, schema_url)

        documentation_urls[resource.id] = (
            f"https://schema.data.gouv.fr/{resource.schema['name']}/latest.html"
        )

    return theme.render(
        'modal.html',
        dataset=dataset,
        documentation_urls=documentation_urls,
        validation_urls=validation_urls,
        authorize_validation=authorize_validation,
    )
