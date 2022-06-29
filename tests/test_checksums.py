import unittest
from app.utils import ga4gh_to_trunc512, trunc512_to_ga4gh
from app.models import Seq
import tests.globals as g


class TestUtils(unittest.TestCase):
    def test_ga4gh_to_trunc512(self):
        result = ga4gh_to_trunc512(ga4gh=g.ga4gh)
        self.assertEqual(result, g.trunc512)

    def test_trunc512_to_ga4gh(self):
        result = trunc512_to_ga4gh(trunc512=g.trunc512)
        self.assertEqual(result, g.ga4gh)

    def test_seq_checksums(self):
        seq = Seq.build_from_seq(g.seq)
        self.assertEqual(seq.ga4gh, g.ga4gh)
        self.assertEqual(seq.md5, g.md5)
