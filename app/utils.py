import base64
import binascii


def ga4gh_to_trunc512(ga4gh):
    digest = base64.urlsafe_b64decode(ga4gh)
    hex_digest = binascii.hexlify(digest)
    return hex_digest.decode("utf-8")


def trunc512_to_ga4gh(trunc512):
    digest = binascii.unhexlify(trunc512)
    ga4gh = base64.urlsafe_b64encode(digest).decode("utf-8")
    return ga4gh
