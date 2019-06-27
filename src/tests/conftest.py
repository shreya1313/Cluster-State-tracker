import pytest
from common.tests.db_fixture import DatabaseFixture


@pytest.fixture
def client():
    from app import application

    db_fixture = DatabaseFixture(application)

    with application.app_context():
        application.config.from_object('settings.test_settings')

        db_fixture.connect_db()

    client = application.test_client()

    yield client

    db_fixture.delete_db()
