import argparse as ap
import csv
import loader
from Bio import SeqIO
from ga4gh.core import sha512t24u
from app.utils import ga4gh_to_trunc512
from hashlib import md5
import sys


def run():
    args = parse_args()
    fasta = args.fasta

    if args.output == "-":
        output = sys.stdout
    else:
        output = open(args.output, mode="w")

    writer = csv.writer(output)
    header = ["id", "ga4gh", "md5"]
    if args.trunc512:
        header.append("trunc512")
    writer.writerow(header)

    _open = loader.guess_parser_from_filname(fasta)
    with _open(fasta) as f:
        for record in SeqIO.parse(f, "fasta"):
            id = record.id
            seq = str(record.seq).encode("ASCII")
            sha512sum = sha512t24u(seq)
            md5sum = md5(seq).hexdigest()
            row = [id, f"SQ.{sha512sum}", md5sum]
            if args.trunc512:
                trunc512sum = ga4gh_to_trunc512(sha512sum)
                row.append(trunc512sum)
            writer.writerow(row)


def parse_args():
    p = ap.ArgumentParser(description="FASTA report generator")
    required = p.add_argument_group("required named arguments")
    required.add_argument(
        "-f",
        "--fasta",
        help="Input FASTA file to load. Supports compressed and uncompressed",
        type=str,
        required=True,
    )
    p.add_argument(
        "--trunc512",
        help="Output trunc512 checksums",
        action="store_true",
        required=False,
        default=False,
    )
    p.add_argument(
        "--output",
        help="Output location. Use - for stdout",
        type=str,
        required=False,
        default="-",
    )
    return p.parse_args()


if __name__ == "__main__":
    run()
