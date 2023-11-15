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

import mimetypes

from .orm import Refget
from .utils import ga4gh_to_trunc512
from flask import (
    request,
    Response,
    jsonify,
    current_app,
    stream_with_context,
    render_template,
)
import re
from flask import Blueprint

refget_blueprint = Blueprint("refget_blueprint", __name__)

INVALID_INPUT = "Invalid input"
RANGE_NS = "Range Not Satisfiable"
BAD_REQUEST = "Bad Request"
INVALID_ENCODING = "Invalid encoding"


@refget_blueprint.route("/")
def index():
    return render_template(
        "index.html", admin=current_app.config.get("ADMIN_INTERFACE")
    )


@refget_blueprint.route("/sequence/service-info", methods=["GET"])
def service_info():

    cfg = current_app.config["SERVICE_INFO"]

    service_info = {
        "id": "org.ga4gh.refget",
        "name": cfg["NAME"],
        "type": {
            "group": "org.ga4gh",
            "artifact": "refget",
            "version": current_app.config["REFGET_VERSION"],
        },
        "description": "Reference sequences from checksums",
        "organization": {
            "name": cfg["ORGANIZATION"]["NAME"],
            "url": cfg["ORGANIZATION"]["URL"],
        },
        "contactUrl": cfg["CONTACT_URL"],
        "documentationUrl": cfg["DOCUMENTATION_URL"],
        "createdAt": cfg["CREATED_AT"],
        "updatedAt": cfg["UPDATED_AT"],
        "environment": cfg["ENVIRONMENT"],
        "version": current_app.config["REFGET_VERSION"],
        "refget": {
            "circular_supported": cfg["REFGET"]["CIRCULAR_SUPPORTED"],
            "subsequence_limit": cfg["REFGET"]["SUBSEQUENCE_LIMIT"],
            "algorithms": cfg["REFGET"]["ALGORITHMS"],
            "identifier_types": cfg["REFGET"]["IDENTIFIER_TYPES"],
        },
    }
    return jsonify(service_info)


@refget_blueprint.route("/sequence/<id>", methods=["GET"])
def sequence(id):
    rg = Refget()
    obj = rg.find_by_id(id)
    if obj == None:
        return "Not Found", 404
    circular = obj.circular
    seq_size = obj.size

    mimetype = request.accept_mimetypes.best_match(
        current_app.config["ACCEPTED_SEQUENCE_VND"]
    )
    if not mimetype:
        return INVALID_ENCODING, 406

    # Have a header but not range object, range is bad
    raw_range = request.headers.get("range")
    if raw_range and request.range is None:
        # But just check it was okay but the wrong way around i.e. start greater than end
        if re.match(r"^bytes=\d+-\d+$", raw_range):
            return RANGE_NS, 416
        return "Invalid request", 400
    # Can only run this if the range parses correctly
    if request.range:
        if "bytes=" not in raw_range:
            return INVALID_INPUT, 400
        (start, end) = request.range.ranges[0]
        if end is None:
            return INVALID_INPUT, 400
        if start < 0 or end < 0:
            return INVALID_INPUT, 400
        if start > end:
            return RANGE_NS, 416
        if start >= seq_size:
            return RANGE_NS, 416
        if end > seq_size:
            end = seq_size
        success = 206
    else:
        try:
            start = int(request.args.get("start", default=0))
        except ValueError:
            return BAD_REQUEST, 400
        try:
            end = request.args.get("end", default=None)
            if end is not None:
                end = int(end)
        except ValueError:
            return BAD_REQUEST, 400
        success = 200

    if start < 0:
        return BAD_REQUEST, 400
    if not circular and end is not None and (start > end):
        return RANGE_NS, 416
    if start >= seq_size:
        return RANGE_NS, 416
    if end is not None:
        if end < 0:
            return BAD_REQUEST, 400
        if end > seq_size:
            return RANGE_NS, 416

    # You can provide a user block size or just take the streamed chunking size from the config
    block_size = int(
        request.args.get("block_size", current_app.config["STREAMED_CHUNKING_SIZE"])
    )
    content_type = "text/vnd.ga4gh.refget.v2.0.0+plain; charset=us-ascii"
    if block_size > 0:
        if end is None:
            end = seq_size

        @stream_with_context
        def generate():
            cur_start = start
            continue_loop = True
            while continue_loop:
                with current_app.app_context():
                    cur_end = cur_start + block_size
                    if cur_end > end:
                        cur_end = end
                        continue_loop = False
                    cur_seq = rg.get_sequence(obj, start=cur_start, end=cur_end)
                    cur_start = cur_end
                    yield cur_seq

        return current_app.response_class(generate(), content_type=content_type)
    else:
        sequence = rg.get_sequence(obj, start=start, end=end)
        return Response(
            sequence,
            status=success,
            content_type=content_type,
        )


@refget_blueprint.route("/sequence/<id>/metadata", methods=["GET"])
def metadata(id):
    accept_match = _get_accept_match()
    if not accept_match:
        return INVALID_ENCODING, 406
    data = _get_metadata(id, accept_match)
    if data == None:
        return "Not Found", 404
    return jsonify({"metadata": data})


def _get_metadata(id, accept_match):
    rg = Refget()
    obj = rg.find_by_id(id)
    if obj == None:
        return None

    data = {
        "length": obj.size,
        "md5": obj.md5,
        "ga4gh": f"SQ.{obj.ga4gh}",
    }

    # Customise to support v1 metadata
    if "vnd.ga4gh.refget.v1" in accept_match:
        data["trunc512"] = ga4gh_to_trunc512(obj.ga4gh)

    data["aliases"] = list(map(_create_aliases, obj.molecules))

    return data


def _get_accept_match():
    return request.accept_mimetypes.best_match(
        current_app.config["ACCEPTED_METADATA_VND"]
    )


@refget_blueprint.route("/sequence/metadata", methods=["POST"])
def metadata_post():
    accept_match = _get_accept_match()
    if not accept_match:
        return INVALID_ENCODING, 406
    json = request.json
    data = {"ids": [], "metadata": []}
    if "ids" in json:
        for id in json["ids"]:
            data["ids"].append(id)
            data["metadata"].append(_get_metadata(id, accept_match=accept_match))
    else:
        return "Bad request", 400
    return jsonify({"metadata": data})


def _create_aliases(molecule):
    return {"alias": molecule.id, "naming_authority": molecule.authority.name}
