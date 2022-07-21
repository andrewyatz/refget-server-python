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

import argparse as ap
import gzip
from mimetypes import guess_type
from functools import partial
from Bio import SeqIO
import sys


def guess_parser_from_filname(fasta):
    encoding = guess_type(fasta)[1]  # uses file extension
    _open = partial(gzip.open, mode="rt") if encoding == "gzip" else open
    return _open


def parse_fasta(fasta, args, rg):
    _open = guess_parser_from_filname(fasta)
    limit = args.commit
    current_count = 0
    total = 0

    with _open(fasta) as f:
        for record in SeqIO.parse(f, "fasta"):
            if current_count == limit:
                print(f"Committing {current_count} record(s)")
                rg.session.commit()
                current_count = 0
            load(record, args, rg)
            current_count = current_count + 1
            total = total + 1

    if current_count > 0:
        print(f"Committing {current_count} record(s) on cleanup")
        rg.session.commit()

    print(f"Loaded {total} FASTA record(s)")


def load(record, args, rg):
    raw_seq, seq_obj = rg.find_or_create_seqs(str(record.seq), circular=False)
    if args.authority is None:
        split_string = record.id.split(":")
        if len(split_string) != 2:
            print(
                f"Cannot process {record.id} because it is not formatted as a CURIE. Use --authority"
            )
            sys.exit(1)
    else:
        authority = args.authority
    mol = rg.create_molecule(
        seq_obj, id=record.id, authority=authority, seq_type=args.type
    )
    rg.session.add_all((raw_seq, seq_obj, mol))
    return raw_seq, mol
