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

import app
from flask_testing import TestCase
from app.models import db
import compliance.db as data
import tests.globals as g


class TestConfig(object):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ECHO = False


class BaseTest(TestCase):
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

    def assert_basic_sequence(
        self,
        id,
        status_code=200,
        seq=None,
        content_type="text/plain",
        range=None,
        query_string={},
    ):
        headers = {"Accept": content_type}
        if range is not None:
            headers["Range"] = range
        response = self.client.get(
            f"/sequence/{id}",
            headers=headers,
            query_string=query_string,
        )
        self.assertEqual(response.status_code, status_code)
        if seq is not None:
            self.assertEqual(response.get_data(as_text=True), seq)

    def assert_basic_metadata(
        self,
        id,
        status_code=200,
        expected=None,
        content_type="application/json",
        query_string={},
    ):
        response = self.client.get(
            f"/sequence/{id}/metadata",
            headers={"Accept": content_type},
            query_string=query_string,
        )
        self.assertEqual(response.status_code, status_code)
        if expected is not None:
            self.assertEqual(response.json, {"metadata": expected})

    def assert_range_sequence(
        self, id, start, end, seq=None, content_type="text/plain", status_code=206
    ):
        range_value = f"bytes={start}-{end}"
        self.assert_basic_sequence(
            id, status_code=status_code, content_type=content_type, seq=seq, range=range_value
        )
