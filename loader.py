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
from app import db, orm


def run():
    args = parse_args()
    rg = orm.Refget(db.session)


def parse_fasta():
    pass


def parse_args():
    p = ap.ArgumentParser(description="FASTA loader for refget")
    required = p.add_argument_group("required named arguments")
    required.add_argument(
        "-f",
        "--file",
        help="Input FASTA file to load. Supports compressed and uncompressed",
        type=str,
        required=True,
    )
    required.add_argument(
        "-t", "--type", help="Sequence type to add", type=str, required=True
    )
    p.add_argument(
        "-a",
        "--authority",
        help="Identifier authority to use. If FASTA sequence IDs are already formatted as CURIEs then do not specify",
        type=str,
    )
    return p.parse_args()


if __name__ == "__main__":
    run()
