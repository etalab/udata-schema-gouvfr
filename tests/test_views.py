import pytest

from flask import render_template_string, current_app

from udata.core.dataset.factories import DatasetFactory, ResourceFactory

import udata_schema_gouvfr.views as schema_views



def render_resource_card(resource):
    return render_template_string(
        '{{ hook("dataset.resource.card.extra-buttons") }}',
        resource=resource
    )


def render_base_modals(dataset):
    return render_template_string('{{ hook("base.modals") }}', dataset=dataset)


@pytest.fixture
def app(app):
    app.register_blueprint(schema_views.blueprint)
    return app


@pytest.fixture(autouse=True)
def mock_catalog(requests_mock):
    requests_mock.get(current_app.config.get('SCHEMA_CATALOG_URL'), json={})


@pytest.mark.frontend
@pytest.mark.usefixtures('clean_db')
@pytest.mark.options(SCHEMA_CATALOG_URL='http://example.com/schemas')
class ViewsTest:
    def test_resource_card_no_resource(self):
        assert '' == render_resource_card(resource=None)

    def test_resource_card_resource_no_schema(self):
        assert '' == render_resource_card(resource=ResourceFactory(schema=None))

    def test_resource_card_resource_with_schema(self):
        resource = ResourceFactory(schema={'name': 'etalab/irve'})

        content = render_resource_card(resource=resource)

        modal_name = f"schemaModalId{str(resource.id).replace('-', '')}"
        assert 'Voir le schéma' in content
        assert f"$refs.{modal_name}" in content

    def test_base_modals_no_dataset(self):
        assert '' == render_base_modals(dataset=None)

    def test_base_modals_dataset_no_schema(self):
        dataset = DatasetFactory(resources=[ResourceFactory(schema={})])
        assert '' == render_base_modals(dataset=dataset)
