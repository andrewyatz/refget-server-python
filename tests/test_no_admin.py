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


class TestConfig(object):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ECHO = False
    ADMIN_INTERFACE = False


class NoAdminTest(TestCase):
    def create_app(self):
        config = TestConfig()
        flask_app = app.create_app(config)
        return flask_app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_no_admin_interface(self):
        response = self.client.get(
            "/admin/stats", headers={"Accept": "application/json"}
        )
        self.assertEqual(response.status_code, 404)
