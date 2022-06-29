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
