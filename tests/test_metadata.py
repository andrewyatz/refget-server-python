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

import copy


class SequenceTests(tests.base.BaseTest):
    def test_metadata(self):
        expected = {
            "md5": g.md5,
            "ga4gh": g.sq,
            "length": len(g.seq),
            "aliases": [{"alias": g.sequence_id, "naming_authority": g.authority}],
        }
        self.assert_basic_metadata(id=g.ga4gh, expected=expected)
        self.assert_basic_metadata(id=g.sq, expected=expected)
        self.assert_basic_metadata(id=g.trunc512, expected=expected)

        # Test v1 support
        v1_expected = copy.deepcopy(expected)
        v1_expected["trunc512"] = g.trunc512
        self.assert_basic_metadata(
            id=g.ga4gh,
            expected=v1_expected,
            content_type="application/vnd.ga4gh.refget.v1.0.1+json; charset=us-ascii",
        )

    def test_bad_metadata(self):
        self.assert_basic_metadata("wibble", status_code=404)
        self.assert_basic_metadata(
            id=g.ga4gh, status_code=406, content_type="plain/text"
        )

    def test_post_metadata(self):
        ids = [g.md5, g.ga4gh, "bogus"]
        expected = {
            "md5": g.md5,
            "ga4gh": g.sq,
            "length": len(g.seq),
            "aliases": [{"alias": g.sequence_id, "naming_authority": g.authority}],
        }
        response = self.client.post(
            "/sequence/metadata",
            headers={"Accept": "application/json"},
            json={"ids": ids},
        )
        data = response.json["metadata"]
        self.assertEqual(len(data["metadata"]), 3)
        # Check IDs array is as expected
        self.assertEqual(data["ids"], ids)
        # Check response of valid queries are as expected
        self.assertEqual(data["metadata"][0], expected)
        self.assertEqual(data["metadata"][1], expected)
        # Third element metadata returned is None
        self.assertEqual(data["metadata"][2], None)


if __name__ == "__main__":
    import unittest

    unittest.main()
