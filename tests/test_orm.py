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
import app.orm as orm
import app.models as models


class OrmTest(tests.base.BaseTest):
    def test_orm_valueset_mod(self):
        rg = orm.Refget()
        with self.assertRaises(ValueError):
            authority = (
                rg.session.query(models.Authority).filter_by(name=g.authority).first()
            )
            self.assertIn(g.authority, str(authority))
            authority.name = "changed"
        self.assertTrue(rg.get_or_create(models.Authority, name=g.authority))
        with self.assertRaises(ValueError):
            seq_type = (
                rg.session.query(models.SeqType).filter_by(name=g.seq_type).first()
            )
            self.assertIn(g.seq_type, str(seq_type))
            seq_type.name = "changed"

    def test_large_objs(self):
        rg = orm.Refget()
        seq = rg.session.query(models.Seq).filter_by(ga4gh=g.sha512t24u).first()
        self.assertIn(g.sha512t24u, str(seq))
        self.assertIn("Seq(", str(seq))
        mol = rg.session.query(models.Molecule).filter_by(seq=seq).first()
        self.assertIn(g.sequence_id, str(mol))
        self.assertIn("Molecule(", str(mol))
        self.assertFalse(mol.circular)
        self.assertEqual(len(g.seq), mol.size)
        self.assertEqual(g.md5, mol.md5)
        self.assertEqual(g.sha512t24u, mol.ga4gh)

    def test_orm(self):
        rg = orm.Refget()
        seq = rg.session.query(models.Seq).filter_by(ga4gh=g.sha512t24u).first()
        mol = rg.session.query(models.Molecule).filter_by(seq=seq).first()
        self.assertIsNone(rg.get_sequence(None))
        self.assertEqual(g.seq, rg.get_sequence(mol))
        self.assertEqual(g.seq[1:], rg.get_sequence(seq, start=1, end=None))
        new_seq = rg.find_by_id(f"{g.authority}:{g.sequence_id}")
        self.assertEqual(g.sha512t24u, new_seq.ga4gh)

    def test_circular(self):
        rg = orm.Refget()
        seq = rg.session.query(models.Seq).filter_by(ga4gh=g.sha512t24u).first()
        seq.circular = True
        circ_seq = rg.get_sequence(seq, start=3, end=1)
        self.assertEqual(g.seq[-1] + g.seq[0], circ_seq)


if __name__ == "__main__":
    import unittest

    unittest.main()
