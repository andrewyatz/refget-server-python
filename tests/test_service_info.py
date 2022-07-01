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

import tests.base


class MyTest(tests.base.BaseTest):
    def test_service_info(self):
        response = self.client.get("/sequence/service-info")
        self.maxDiff = None
        expected = {
            "id": "org.ga4gh.refget",
            "name": "Refget Reference Implementation Server",
            "type": {"group": "org.ga4gh", "artifact": "refget", "version": "2.0.0"},
            "description": "Reference sequences from checksums",
            "organization": {"name": "GA4GH", "url": "https://www.ga4gh.org"},
            "contactUrl": "https://github.com/ga4gh/refget-server-python",
            "documentationUrl": "https://github.com/ga4gh/refget-server-python",
            "createdAt": "2022-06-29T12:58:19Z",
            "updatedAt": "2022-06-29T12:58:19Z",
            "environment": "prod",
            "version": "2.0.0",
            "refget": {
                "circular_supported": True,
                "subsequence_limit": None,
                "algorithms": [
                    "ga4gh",
                    "md5",
                    "trunc512",
                ],
                "identifier_types": [
                    "insdc",
                    "none",
                ],
            },
        }
        self.assert200(response)
        self.assertEqual(response.json, expected)
