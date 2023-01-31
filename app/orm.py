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

from . import models as m
from .models import db
from sqlalchemy import func
from .utils import trunc512_to_ga4gh


class Refget:
    def __init__(self) -> None:
        self.session = db.session

    """
	Search for a sequence by an identifier. Supports ga4gh:SQ., md5 or another CURIE formatted ID e.g. refseq:NM_001354609.2
	"""

    def find_by_id(self, id: str):
        # Trigger ga4gh checks
        if "ga4gh:SQ." in id:
            ga4gh = id.replace("ga4gh:SQ.", "")
            return self.session.query(m.Seq).filter(m.Seq.ga4gh == ga4gh).first()
        # It is md5 then
        elif "md5:" in id:
            md5 = id.replace("md5:", "")
            return self.session.query(m.Seq).filter(m.Seq.md5 == md5.lower()).first()
        # Assume authority ID query
        elif ":" in id:
            authority, split_id = id.split(":")
            molecule = self.find_molecule(split_id, authority)
            if molecule is None:
                return None
            return molecule.seq
        elif "SQ." in id:
            ga4gh = id.replace("SQ.", "")
            return self.session.query(m.Seq).filter(m.Seq.ga4gh == ga4gh).first()
        # Assume md5
        elif len(id) == 32:
            return self.session.query(m.Seq).filter(m.Seq.md5 == id.lower()).first()
        # Test if it is trunc512 and give backwards compatability
        elif len(id) == 48:
            ga4gh = trunc512_to_ga4gh(id)
            return self.session.query(m.Seq).filter(m.Seq.ga4gh == ga4gh).first()
        else:
            return None

    """
    Find a molecule by a sequence identifier
    """

    def find_molecule(self, id, authority):
        return (
            self.session.query(m.Molecule)
            .join(m.Authority)
            .join(m.Seq)
            .filter(m.Molecule.id == id, m.Authority.name == authority)
            .first()
        )

    """
    Retrieve sequence from the raw_seq table

    Params:
        obj: models.Seq object to query by. Can also provide a models.Molecule and code will understand this
        start: start in 0-based coordinate space. Default is 0
        end: end in 1-based coordinate space (inclusive of end). Default is None
    """

    def get_sequence(self, obj, start=0, end=None):
        if type(obj) == m.Seq:
            seq = obj
        elif type(obj) == m.Molecule:
            seq = obj.seq
        else:
            return None

        # If we are in this situation
        if end is not None and start > end and seq.circular:
            subseq = self._get_sequence(seq, start, seq.size)
            subseq_two = self._get_sequence(seq, 0, end)
            return subseq + subseq_two
        # Normal operation on linear sequence
        else:
            return self._get_sequence(seq, start=start, end=end)

    def _get_sequence(self, seq, start=0, end=None):
        # If we didn't specify anything return the sequence
        if start == 0 and end == None:
            rawseq = (
                self.session.query(m.RawSeq).filter(m.RawSeq.ga4gh == seq.ga4gh).first()
            )
            return rawseq.seq
        # Otherwise we need to substring
        else:
            if end is None:
                end = seq.size
            length = end - start
            substr_start = start + 1
            db_seq = (
                self.session.query(
                    func.substr(m.RawSeq.seq, substr_start, length),
                )
                .filter(m.RawSeq.ga4gh == seq.ga4gh)
                .first()
            )
            return db_seq[0]

    """
    Create a molecule and sub-objects from parameters

    Params:
        seq: Raw sequence data
        id: The identifier to use for this sequence/molecule
        authority: The issuing authority for the identifier
        seq_type: Sequence type to use
    
    Returns:
        Fully formed molecule
    """

    def create_molecule(self, seq_obj, id, authority, seq_type):
        auth_obj = self.get_or_create(m.Authority, name=authority)
        seq_type_obj = self.get_or_create(m.SeqType, name=seq_type)
        mol = self.find_molecule(id, authority)
        if mol is None:
            mol = m.Molecule(
                seq=seq_obj, id=id, authority=auth_obj, seq_type=seq_type_obj
            )
        return mol

    def find_or_create_seqs(self, seq, circular=False):
        seq_obj = m.Seq.build_from_seq(seq=seq, circular=circular)
        rawseq_instance = (
            self.session.query(m.RawSeq).filter_by(ga4gh=seq_obj.ga4gh).first()
        )
        if not rawseq_instance:
            rawseq_instance = m.RawSeq(seq=seq, ga4gh=seq_obj.ga4gh)
        seq_instance = (
            self.session.query(m.Seq).filter_by(ga4gh=seq_obj.ga4gh)
        ).first()
        if not seq_instance:
            seq_instance = seq_obj
        return rawseq_instance, seq_instance

    def get_or_create(self, model, **kwargs):
        instance = self.session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            return instance
