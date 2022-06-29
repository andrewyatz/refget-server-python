import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REFGET_VERSION = "2.0.0"
    TEXT_CONTENT_TYPE_VND = (
        f"text/vnd.ga4gh.refget.v{REFGET_VERSION}+plain; charset=us-ascii"
    )
    JSON_CONTENT_TYPE_VND = (
        f"application/vnd.ga4gh.refget.v{REFGET_VERSION}+json; charset=us-ascii"
    )
    ACCEPTED_SEQUENCE_VND = [
        TEXT_CONTENT_TYPE_VND,
        f"text/vnd.ga4gh.refget.v{REFGET_VERSION}+plain",
        f"text/vnd.ga4gh.refget.v{REFGET_VERSION}+plain",
        f"text/vnd.ga4gh.refget.v1.0.0+plain",
        f"text/vnd.ga4gh.refget.v1.0.0+plain; charset=us-ascii",
        "text/plain",
    ]
    ACCEPTED_METADATA_VND = [
        JSON_CONTENT_TYPE_VND,
        f"application/vnd.ga4gh.refget.v{REFGET_VERSION}+json",
        f"application/vnd.ga4gh.refget.v{REFGET_VERSION}+json",
        f"application/vnd.ga4gh.refget.v1.0.0+json",
        f"application/vnd.ga4gh.refget.v1.0.0+json; charset=us-ascii"
        "application/json",
    ]
