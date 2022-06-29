from attr import Attribute
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    validates,
)

import hashlib
from app import db
from ga4gh.core import sha512t24u

# create declarative_base instance
Base = declarative_base()


class RawSeq(db.Model):
    __tablename__ = "raw_seq"
    ga4gh = Column(String(32), primary_key=True)
    seq = Column(String, nullable=False)


class Seq(db.Model):
    __tablename__ = "seq"

    seq_id = Column(Integer, primary_key=True)
    md5 = Column(String(32), nullable=False, index=True)
    ga4gh = Column(String(32), nullable=False, unique=True, index=True)
    size = Column(Integer, nullable=False)
    circular = Column(Boolean, nullable=False)
    molecules = relationship("Molecule", back_populates="seq", lazy="joined")

    def __repr__(self):
        return "<Seq(md5='%s', ga4gh='%s', size='%d', circular='%s')>" % (
            self.md5,
            self.ga4gh,
            self.size,
            self.circular,
        )

    """
	Builder method which creates a Seq instance from a sequence string

	Args:
		seq: String sequence data
		circular: Indicates if the Seq is circular. Defaults to False
	
	Returns:
		A Seq object populated with md5 & ga4gh identifiers
	"""

    def build_from_seq(seq: str, circular=False):
        ga4gh = sha512t24u(seq.encode("utf-8"))
        md5 = hashlib.md5(seq.encode("utf-8")).hexdigest()
        size = len(seq)
        return Seq(md5=md5, ga4gh=ga4gh, size=size, circular=circular)


class Molecule(db.Model):
    __tablename__ = "molecule"

    molecule_id = Column(Integer, primary_key=True)
    seq_id = Column(Integer, ForeignKey("seq.seq_id"))
    id = Column(String, nullable=False)
    authority_id = Column(Integer, ForeignKey("authority.authority_id"))
    seq_type_id = Column(Integer, ForeignKey("seq_type.seq_type_id"))

    authority = relationship("Authority", lazy="joined")
    seq_type = relationship("SeqType", lazy="joined")
    seq = relationship("Seq")

    __table_args__ = (
        UniqueConstraint("id", "authority_id", name="molecule_uix_id_authority"),
    )

    def __getattr__(self, attribute):
        if attribute == "circular":
            return self.seq.circular
        elif attribute == "size":
            return self.seq.size
        elif attribute == "ga4gh":
            return self.seq.size
        elif attribute == "md5":
            return self.seq.md5
        raise AttributeError(f"'Molecule' object has no attribute '{attribute}'")

    def __repr__(self):
        return "<Molecule(seq='%s', id='%s', authority='%s')>" % (
            self.seq,
            self.id,
            self.authority,
        )


class Authority(db.Model):
    __tablename__ = "authority"

    authority_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True, unique=True)

    @validates("name")
    def validates_name(self, key, value):
        if self.name:
            raise ValueError("Authority name cannot be modified")
        return value

    def __repr__(self):
        return "<Authority(name='%s')>" % self.name


class SeqType(db.Model):
    __tablename__ = "seq_type"

    seq_type_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True, unique=True)

    @validates("name")
    def validates_name(self, key, value):
        if self.name:
            raise ValueError("Type name cannot be modified")
        return value

    def __repr__(self):
        return "<SeqType(name='%s')>" % self.name
