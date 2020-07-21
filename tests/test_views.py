import pytest

from flask import Blueprint, render_template_string, url_for
from udata.tests.helpers import assert200

import udata_schema.views as schema_views

bp = Blueprint('views_test', __name__, url_prefix='/views_test')


@bp.route('/resource_card')
def render_resource_card():
    return render_template_string('{{ hook("dataset.resource.card.extra-buttons") }}')


@bp.route('/base_modals')
def render_base_modals():
    return render_template_string('{{ hook("base.modals") }}')


@pytest.fixture
def app(app):
    app.register_blueprint(schema_views.blueprint)
    app.register_blueprint(bp)
    return app


@pytest.mark.frontend
class ViewsTest:
    def test_resource_card_no_schema(self, client):
        response = client.get(url_for('views_test.render_resource_card'))
        assert200(response)
        assert b'' == response.data
