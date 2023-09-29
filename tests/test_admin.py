# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tests.globals as g
from app.models import db
import app
from flask_testing import TestCase
import compliance.db as data


class TestConfig(object):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ECHO = False
    ADMIN_INTERFACE = True


class AdminTests(TestCase):
    def create_app(self):
        config = TestConfig()
        flask_app = app.create_app(config)
        return flask_app

    def setUp(self):
        db.create_all()
        with db.session.begin():
            seq, mol = data.create(g.seq, g.sequence_id, g.authority, g.seq_type, False)
            db.session.add_all([seq, mol])

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_stats(self):
        expected = {"counts": {"seqs": 1, "molecules": 1}}
        response = self.client.get(
            "/admin/stats", headers={"Accept": "application/json"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected)


if __name__ == "__main__":
    import unittest

    unittest.main()
