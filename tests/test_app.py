import unittest
from flask_testing import TestCase
from app.models import db
import compliance.db as data
import tests.globals as g

import app


class TestConfig(object):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ECHO = False


class MyTest(TestCase):
    def create_app(self):
        config = TestConfig()
        flask_app = app.create_app(config)
        return flask_app

    def test_service_info(self):
        response = self.client.get("/sequence/service-info")
        expected = {
            "service": {
                "algorithms": ["md5", "ga4gh", "trunc512"],
                "circular_supported": True,
                "subsequence_limit": None,
                "supported_api_versions": ["2.0.0"],
            },
        }
        self.assertEqual(response.json, expected)

    def test_sequence(self):
        response = self.client.get(
            f"/sequence/ga4gh:SQ.{g.ga4gh}", headers={"Accept": "text/plain"}
        )
        self.assert200(response)
        self.assertEqual(response.get_data(as_text=True), g.seq)

    def setUp(self):
        db.create_all()
        with db.session.begin():
            seq, mol = data.create(g.seq, "id", "test", "dna", False)
            db.session.add_all([seq, mol])
        # data.populate(silent=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()
