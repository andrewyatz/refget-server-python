from app import orm
from app.models import db
import requests

rg = orm.Refget()


def populate(silent=False):
    with rg.session.begin():
        db.create_all()
        if not silent:
            print("Load Enterobacteria phage phiX174 sensu lato")
        _load(
            "3332ed720ac7eaa9b3655c06f6b9e196",
            id="NC_001422.1",
            authority="insdc",
            seq_type="dna",
            circular=True,
        )
        if not silent:
            print("Load S.cer chr I")
        _load("6681ac2f62509cfc220d78751b8dc524", "BK006935.2", "insdc", "dna")
        if not silent:
            print("Load S.cer chr VI")
        _load("b7ebc601f9a7df2e1ec5863deeae88a3", "BK006940.2", "insdc", "dna")
        if not silent:
            print("Load ACGT")
        raw_seq, mol = create("ACGT", "basic", "none", "dna", False)
        rg.session.add_all((raw_seq, mol))
        rg.session.commit()


def create(seq, id, authority, seq_type="dna", circular=False):
    raw_seq, seq_obj = rg.find_or_create_seqs(seq, circular=circular)
    mol = rg.create_molecule(seq_obj, id=id, authority=authority, seq_type=seq_type)
    rg.session.add_all((raw_seq, seq_obj, mol))
    return raw_seq, mol


def _load(checksum, id, authority, seq_type, circular=False):
    ena_refget = "https://www.ebi.ac.uk/ena/cram/sequence"
    r = requests.get(f"{ena_refget}/{checksum}")
    seq = r.text
    raw_seq, mol = create(seq, id, authority, seq_type, circular=circular)
    rg.session.add_all([raw_seq, mol])
