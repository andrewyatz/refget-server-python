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

import base64
import binascii


def ga4gh_to_trunc512(ga4gh):
    digest = base64.urlsafe_b64decode(ga4gh)
    hex_digest = binascii.hexlify(digest)
    return hex_digest.decode("utf-8").lower()


def trunc512_to_ga4gh(trunc512):
    digest = binascii.unhexlify(trunc512)
    ga4gh = base64.urlsafe_b64encode(digest).decode("utf-8")
    return ga4gh
