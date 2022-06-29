from app import db, orm
import requests

rg = orm.Refget(db.session)


def populate():
    with db.session.begin():
        db.create_all()
        print("Load Enterobacteria phage phiX174 sensu lato")
        load(
            "3332ed720ac7eaa9b3655c06f6b9e196",
            id="NC_001422.1",
            authority="insdc",
            seq_type="dna",
            circular=True,
        )
        print("Load S.cer chr I")
        load("6681ac2f62509cfc220d78751b8dc524", "BK006935.2", "insdc", "dna")
        print("Load S.cer chr VI")
        load("b7ebc601f9a7df2e1ec5863deeae88a3", "BK006940.2", "insdc", "dna")
        print("Load ACGT")
        raw_seq, seq_obj = rg.find_or_create_seqs("ACGT")
        mol = rg.create_molecule(seq_obj, id="basic", authority="none", seq_type="dna")
        db.session.add_all((raw_seq, seq_obj, mol))
        db.session.commit()


def load(checksum, id, authority, seq_type, circular=False):
    ena_refget = "https://www.ebi.ac.uk/ena/cram/sequence"
    r = requests.get(f"{ena_refget}/{checksum}")
    seq = r.text
    raw_seq, seq_obj = rg.find_or_create_seqs(seq, circular=circular)
    mol = rg.create_molecule(seq_obj, id=id, authority=authority, seq_type=seq_type)
    db.session.add_all([raw_seq, mol])
