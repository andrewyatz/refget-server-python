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


class SequenceTests(tests.base.BaseTest):
    def test_sequence(self):
        self.assert_basic_sequence_fetch(g.ga4gh)
        self.assert_basic_sequence_fetch(g.sq)
        self.assert_basic_sequence_fetch(g.md5)
        self.assert_basic_sequence_fetch(f"md5:{g.md5}")
        self.assert_basic_sequence_fetch(g.md5.upper())
        self.assert_basic_sequence_fetch(g.trunc512)
        self.assert_basic_sequence_fetch(g.trunc512.upper())

        # Fancy content types
        self.assert_basic_sequence_fetch(
            g.ga4gh, content_type="text/vnd.ga4gh.refget.v2.0.0+plain"
        )
        self.assert_basic_sequence_fetch(
            g.ga4gh, content_type="text/vnd.ga4gh.refget.v1.0.0+plain"
        )
        self.assert_basic_sequence_fetch(
            g.ga4gh, content_type="text/vnd.ga4gh.refget.v2.0.0+plain; charset=us-ascii"
        )
        self.assert_basic_sequence(
            g.ga4gh, status_code=200, query_string={"block_size": 2}
        )

    def assert_basic_sequence_fetch(self, id, content_type="text/plain"):
        self.assert_basic_sequence(
            id, status_code=200, seq=g.seq, content_type=content_type
        )

    def test_bad_sequence(self):
        self.assert_basic_sequence("wibble", status_code=404)
        self.assert_basic_sequence(f"ga4gh.SQ:{g.sha512t24u}", status_code=404)
        self.assert_basic_sequence(f"ga4gh.SQ:{g.sha512t24u}", status_code=404)
        self.assert_basic_sequence(
            g.ga4gh, status_code=416, query_string={"start": 1000}
        )
        self.assert_basic_sequence(g.ga4gh, status_code=406, content_type="text/html")

    def test_sequence_ranges(self):
        self.assert_basic_sequence(
            g.ga4gh, seq="AC", query_string={"start": 0, "end": 2}
        )

    def test_get_range_sequence_fetch(self):
        self.assert_range_sequence(g.ga4gh, 0, 2, "ACG")
        self.assert_range_sequence(g.ga4gh, 0, 2, "ACG")
        self.assert_range_sequence(g.ga4gh, 0, 4, "ACGT")

    def test_bad_range_sequence_fetch(self):
        self.assert_range_sequence(g.ga4gh, -1, 2, status_code=400)
        self.assert_range_sequence(g.ga4gh, 1, -2, status_code=400)
        self.assert_range_sequence(g.ga4gh, 3, 2, status_code=416)
        self.assert_range_sequence(g.ga4gh, 4, 4, status_code=416)
        self.assert_basic_sequence(g.ga4gh, status_code=400, range="wibble=1-2")
        self.assert_basic_sequence(g.ga4gh, status_code=400, range="bytes=1-")
        self.assert_basic_sequence(g.ga4gh, status_code=400, range="bytes=1-")
        self.assert_basic_sequence(g.ga4gh, status_code=400, range="bytes=-1-2")
        self.assert_basic_sequence(g.ga4gh, status_code=400, range="bytes=a-a")

    def test_bad_url_parameter_fetch(self):
        self.assert_basic_sequence(
            g.ga4gh, query_string={"start": "wibble", "end": 1}, status_code=400
        )
        self.assert_basic_sequence(
            g.ga4gh, query_string={"start": 0, "end": "wibble"}, status_code=400
        )
        self.assert_basic_sequence(
            g.ga4gh, query_string={"start": -1, "end": 1}, status_code=400
        )
        self.assert_basic_sequence(
            g.ga4gh, query_string={"start": -20, "end": -1}, status_code=400
        )
        self.assert_basic_sequence(g.ga4gh, query_string={"end": -1}, status_code=416)
        self.assert_basic_sequence(
            g.ga4gh, query_string={"start": 0, "end": 100}, status_code=416
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
