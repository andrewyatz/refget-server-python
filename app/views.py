# from app import app
# from . import db
import mimetypes
from .orm import Refget
from .utils import ga4gh_to_trunc512
from flask import request, Response, jsonify, current_app
import re
from flask import Blueprint

refget_blueprint = Blueprint("refget_blueprint", __name__)


@refget_blueprint.route("/")
def index():
    return "Hello"


@refget_blueprint.route("/sequence/service-info", methods=["GET"])
def service_info():

    data = {
        "service": {
            "circular_supported": True,
            "algorithms": ["md5", "ga4gh", "trunc512"],
            "subsequence_limit": None,
            "supported_api_versions": [current_app.config["REFGET_VERSION"]],
        }
    }
    return jsonify(data)


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
        return "Invalid encoding", 406

    # Have a header but not range object, range is bad
    raw_range = request.headers.get("range")
    if raw_range and request.range is None:
        # But just check it was okay but the wrong way around i.e. start greater than end
        if re.match(r"^bytes=\d+-\d+$", raw_range):
            return "Range Not Satisifable", 416
        return "Invalid request", 400
    # Can only run this if the range parses correctly
    if request.range:
        if "bytes=" not in raw_range:
            return "Invalid input", 400
        (start, end) = request.range.ranges[0]
        if end is None:
            return "Invalid input", 400
        if start < 0 or end < 0:
            return "Invalid input", 400
        if start > end:
            return "Range Not Satisfiable", 416
        if start >= seq_size:
            return "Range Not Satisfiable", 416
        if end > seq_size:
            end = seq_size
        success = 206
    else:
        try:
            start = int(request.args.get("start", default=0))
        except ValueError:
            return "Bad request", 400
        try:
            end = request.args.get("end", default=None)
            if end is not None:
                end = int(end)
        except ValueError:
            return "Bad request", 400
        success = 200

    if start < 0:
        return "Bad Request", 400
    if not circular and not end is None and (start > end):
        return "Range Not Satisfiable", 416
    if start >= seq_size:
        return "Range Not Satisfiable", 416
    if not end is None:
        if end < 0:
            return "Bad Request", 400
        if end > seq_size:
            return "Range Not Satisfiable", 416

    sequence = rg.get_sequence(obj, start=start, end=end)
    return Response(
        sequence,
        status=success,
        content_type="text/vnd.ga4gh.refget.v2.0.0+plain; charset=us-ascii",
    )


@refget_blueprint.route("/sequence/<id>/metadata", methods=["GET"])
def metadata(id):
    accept_match = request.accept_mimetypes.best_match(
        current_app.config["ACCEPTED_METADATA_VND"]
    )
    if not accept_match:
        return "Invalid encoding", 406

    rg = Refget()
    obj = rg.find_by_id(id)
    if obj == None:
        return "Not Found", 404

    data = {
        "length": obj.size,
        "md5": obj.md5,
        "ga4gh": f"ga4gh.SQ:{obj.ga4gh}",
        "id": id,
    }

    # Customise to support v1 metadata
    if "vnd.ga4gh.refget.v1.0.0" in accept_match:
        data["trunc512"] = ga4gh_to_trunc512(obj.ga4gh)

    data["aliases"] = list(map(_create_aliases, obj.molecules))

    return jsonify({"metadata": data})


def _create_aliases(molecule):
    return {"alias": molecule.id, "naming_authority": molecule.authority.name}
