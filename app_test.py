import logging
import os

import flask_migrate
import pytest

from app import app

logging.basicConfig(level=logging.INFO)


@pytest.fixture()
def app_fixture():
    app.config['TESTING'] = True

    with app.app_context():
        yield


def test_logging(app_fixture, caplog):
    msg1 = "Before"
    logging.info(msg1)

    if os.getenv('DO_UPGRADE'):
        flask_migrate.upgrade()

    msg2 = "After"
    logging.info(msg2)
    assert [msg1, msg2] == [rec.message for rec in caplog.records]
