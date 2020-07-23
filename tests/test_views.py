import pytest

from flask import render_template_string

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


@pytest.mark.frontend
@pytest.mark.usefixtures('clean_db')
class ViewsTest:
    def test_resource_card_no_resource(self):
        assert '' == render_resource_card(resource=None)

    def test_resource_card_resource_no_schema(self):
        assert '' == render_resource_card(resource=ResourceFactory(schema=None))

    def test_resource_card_resource_with_schema(self):
        resource = ResourceFactory(schema='etalab/irve')

        content = render_resource_card(resource=resource)

        modal_name = f"schemaModalId{str(resource.id).replace('-', '')}"
        assert 'Voir le schéma' in content
        assert f"$refs.{modal_name}" in content

    def test_base_modals_no_dataset(self):
        assert '' == render_base_modals(dataset=None)

    def test_base_modals_dataset_no_schema(self):
        dataset = DatasetFactory(resources=[ResourceFactory(schema=None)])
        assert '' == render_base_modals(dataset=dataset)

    @pytest.mark.options(SCHEMA_GOUVFR_VALIDATA_URL='https://validata.example.com')
    def test_base_modals_dataset_w_schema(self):
        resource = ResourceFactory(schema='etalab/irve')
        dataset = DatasetFactory(resources=[resource])

        content = render_base_modals(dataset=dataset)

        assert 'etalab/irve' in content
        assert f"schema-modal-Id{str(resource.id).replace('-', '')}" in content
        assert 'https://validata.example.com/table-schema' in content
        assert 'https://schema.data.gouv.fr' in content

    def test_base_modals_dataset_w_schemas(self):
        dataset = DatasetFactory(resources=[
            ResourceFactory(schema='etalab/irve'),
            ResourceFactory(schema='etalab/covoiturage'),
        ])

        content = render_base_modals(dataset=dataset)

        assert 'etalab/irve' in content
        assert 'etalab/covoiturage' in content
        assert 2 == content.count('</modal>')
