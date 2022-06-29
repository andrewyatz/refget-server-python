import tests.globals as g
import tests.base

import app


class SequenceTests(tests.base.BaseTest):
    def test_sequence(self):
        self.assert_basic_sequence_fetch(g.ga4gh)
        self.assert_basic_sequence_fetch(g.md5)
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
        self.assert_range_sequence(g.ga4gh, 0, 4, "ACGT")


if __name__ == "__main__":
    unittest.main()
