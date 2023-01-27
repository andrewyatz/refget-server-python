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

import unittest
from app.utils import ga4gh_to_trunc512, trunc512_to_ga4gh
from app.models import Seq
import tests.globals as g


class TestUtils(unittest.TestCase):
    def test_ga4gh_to_trunc512(self):
        result = ga4gh_to_trunc512(ga4gh=g.sha512t24u)
        self.assertEqual(result, g.trunc512)

    def test_trunc512_to_ga4gh(self):
        result = trunc512_to_ga4gh(trunc512=g.trunc512)
        self.assertEqual(result, g.sha512t24u)

    def test_seq_checksums(self):
        seq = Seq.build_from_seq(g.seq)
        self.assertEqual(seq.ga4gh, g.sha512t24u)
        self.assertEqual(seq.md5, g.md5)


if __name__ == "__main__":
    import unittest

    unittest.main()
