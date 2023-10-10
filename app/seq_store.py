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

"""
Set of classes concerned with storing sequences. The default implementation
writes to the raw_seq table. Other implementations may consider switching
storage to other layers
"""


class SeqStore:

    """
    Store a sequence object alongside its given checksum in the
    backend store. Must be implemented
    """

    def store(self, checksum, seq):
        raise NotImplementedError()

    """
    Interface method for retriving sequence. Delegates onto
    internal method for subseq retrieval for actual retrieval. Also implements
    circular chromosome logic

    Params:
        seq_obj: models.Seq object to query by
        start: start in 0-based coordinate space. Default is 0
        end: end in 1-based coordinate space (inclusive of end). Default is None
    """

    def get_seq(self, seq_obj, start=0, end=None):

        size = seq_obj.size
        if end is None:
            end = size

        # We are in a circular sequence call
        if start > end and seq_obj.circular:
            subseq = self._sub_seq(seq_obj, start, (size - start))
            subseq += self._sub_seq(seq_obj, 0, end)
            sequence = subseq
        else:
            length = end - start
            sequence = self._sub_seq(seq_obj, start, length)

        return sequence

    """
    Subsequence method to be implemneted

    Params:
        seq_obj: seq object to query for
        start: start in 0-based coordinate space. Default is 0
        length: length of the sequence to fetch
    """

    def _sub_seq(self, seq_obj, start, length):
        raise NotImplementedError()


"""
Basic implementation which uses the raw_seq table to store sequence. Assumes
that a sequence will never be bigger than the limitaitons imposed upon it
by the target database infrastructure.

Note that PostgreSQL has a max size of 1GB for a text field and MySQL's maximum
allowed packet size is also 1GB. If you need to store very large sequences 
you should switch to the ChunkedSeqStore implementation.
"""


class RawSeqStore(SeqStore):
    def __init__(self) -> None:
        self.session = db.session

    def store(self, checksum, seq):
        rawseq_instance = self.session.query(m.RawSeq).filter_by(ga4gh=checksum).first()
        if rawseq_instance is None:
            rawseq_instance = m.RawSeq(seq=seq, ga4gh=checksum)
        return rawseq_instance

    def _sub_seq(self, seq, start, length):
        if length == seq.size:
            rawseq = (
                self.session.query(m.RawSeq).filter(m.RawSeq.ga4gh == seq.ga4gh).first()
            )
            return rawseq.seq
        # Otherwise we need to substring
        else:
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
Version of the RawSeq store which stores sequences as a series of blocks. By
default we store in blocks of 134,217,728bp. You can control this by
providing an alternative chunk_power. Calculate the size by executing 1 << chunk_power.

Common sizes from their powers are:

16 : 65,536
17 : 131,072
18 : 262,144
19 : 524,288
20 : 1,048,576
21 : 2,097,152
21 : 2,097,152
22 : 4,194,304
23 : 8,388,608
24 : 16,777,216
25 : 33,554,432
26 : 67,108,864
27 : 134,217,728
28 : 268,435,456
29 : 536,870,912

Pick a value which is a good match between minimising the need to create too many chunks
but also supported well by your database technology of choice.

"""


class ChunkedRawSeq(SeqStore):
    def __init__(self, chunk_power=27) -> None:
        self.chunk_power = chunk_power
        self.session = db.session

    def store(self, checksum, seq):
        power = self.chunk_power
        length = len(seq)
        chunk = 1 << power
        iterations = math.ceil(length / chunk)
        created_chunks = []
        for i in range(0, iterations):
            start = chunk * i
            end = start + chunk
            if end > length:
                end = length
            seq_chunk = seq[start:end]
            chunk_length = len(seq_chunk)
            new_chunk = m.ChunkedRawSeq(
                seq=seq_chunk,
                length=chunk_length,
                offset=start,
                block=i,
                ga4gh=checksum,
            )
            created_chunks.append(new_chunk)
        return created_chunks

    def _sub_seq(self, seq_obj, start, length):
        power = self.chunk_power
        substr_end = start + length
        start_bin = start >> power
        end_bin = substr_end >> power
        concat_string = ""
        for bin in range(start_bin, end_bin):
            virtual_start = bin << power
            virtual_end = bin + 1 << power
            print(
                f"bin:{bin}|v_start:{virtual_start}|v_end:{virtual_end}|substr_start:{start}|substr_end:{substr_end}"
            )
            if bin == start_bin:
                local_start = start - virtual_start
                local_length = virtual_end - start
                if substr_end < virtual_end:
                    local_length = length
                concat_string += self._perform_remote_substring(
                    seq_obj, local_start, local_length
                )
            elif bin == end_bin:
                local_start = 0
                local_length = substr_end - virtual_start
                concat_string += self._perform_remote_substring(
                    seq_obj, local_start, local_length
                )
            else:
                # we can just grab the entire seq and concat
                concat_string += self._perform_remote_substring(
                    seq_obj, 0, (1 << power)
                )
        return concat_string

    def _perform_remote_substring(self, seq_obj, start, length):
        substr_start = start + 1
        db_seq = (
            self.session.query(
                func.substr(m.ChunkedRawSeq.seq, substr_start, length),
            )
            .filter(m.ChunkedRawSeq.ga4gh == seq_obj.ga4gh)
            .first()
        )
        return db_seq[0]
