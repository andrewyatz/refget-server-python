import tests.globals as g
import tests.base

import app


class SequenceTests(tests.base.BaseTest):
    def test_metadata(self):
      response = self.client.get(f"/sequence/{g.ga4gh}/metadata", headers={"Accept":"application/json"})
      expected = {
          "md5" : g.md5,
          "ga4gh" : g.ga4gh,
          "id" : g.ga4gh,
          "length" : len(g.seq),
          "aliases" : [
            {
              "alias" : g.sequence_id,
              "naming_authority" : g.authority
            }
          ]
      }
      self.assert200(response)
      self.assertEqual(response.json, { "metadata" : expected })