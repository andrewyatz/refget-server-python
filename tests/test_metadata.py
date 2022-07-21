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
import tests.base

import app


class SequenceTests(tests.base.BaseTest):
    def test_metadata(self):
        response = self.client.get(
            f"/sequence/{g.ga4gh}/metadata", headers={"Accept": "application/json"}
        )
        expected = {
            "md5": g.md5,
            "ga4gh": g.ga4gh,
            "length": len(g.seq),
            "aliases": [{"alias": g.sequence_id, "naming_authority": g.authority}],
        }
        self.assert200(response)
        self.assertEqual(response.json, {"metadata": expected})
