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

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        basedir, os.pardir, "compliance.sqlite3"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    STREAMED_CHUNKING_SIZE = 0

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
        f"application/vnd.ga4gh.refget.v1.0.0+json; charset=us-ascii",
        "application/json",
    ]
    SERVICE_INFO = {
        "NAME": "Refget Reference Implementation Server",
        "ORGANIZATION": {"NAME": "GA4GH", "URL": "https://www.ga4gh.org"},
        "CONTACT_URL": "https://github.com/ga4gh/refget-server-python",
        "DOCUMENTATION_URL": "https://github.com/ga4gh/refget-server-python",
        "CREATED_AT": "2022-06-29T12:58:19Z",
        "UPDATED_AT": "2022-06-29T12:58:19Z",
        "ENVIRONMENT": "prod",
        "VERSION": REFGET_VERSION,
        "REFGET": {
            "CIRCULAR_SUPPORTED": True,
            "SUBSEQUENCE_LIMIT": None,
            "ALGORITHMS": ["ga4gh", "md5", "trunc512"],
            "IDENTIFIER_TYPES": ["insdc", "none"],
        },
    }

    CORS = {
        "METHODS": ["GET", "HEAD", "OPTIONS"],
        "ALLOW_HEADERS": [
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "api_key",
            "Range",
        ],
        "EXPOSE_HEADERS": [
            "Cache-Control",
            "Content-Language",
            "Content-Type",
            "Expires",
            "Last-Modified",
            "Pragma",
        ],
        "MAX_AGE": 2592000,
    }
