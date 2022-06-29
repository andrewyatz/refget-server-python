import unittest
from app.utils import ga4gh_to_trunc512, trunc512_to_ga4gh
from app.models import Seq


class TestUtils(unittest.TestCase):
    ga4gh = "aKF498dAxcJAqme6QYQ7EZ07-fiw8Kw2"
    trunc512 = "68a178f7c740c5c240aa67ba41843b119d3bf9f8b0f0ac36"
    md5 = "f1f8f4bf413b16ad135722aa4591043e"
    seq = "ACGT"

    def test_ga4gh_to_trunc512(self):
        result = ga4gh_to_trunc512(ga4gh=self.ga4gh)
        self.assertEqual(result, self.trunc512)

    def test_trunc512_to_ga4gh(self):
        result = trunc512_to_ga4gh(trunc512=self.trunc512)
        self.assertEqual(result, self.ga4gh)

    def test_seq_checksums(self):
        seq = Seq.build_from_seq(self.seq)
        self.assertEqual(seq.ga4gh, self.ga4gh)
        self.assertEqual(seq.md5, self.md5)


if __name__ == "__main__":
    unittest.main()
