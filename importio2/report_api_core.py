#
# Copyright 2018 Import.io
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
#

import logging
import os
import requests


logger = logging.getLogger(__name__)

"""
Low-level REST API calls that specify the inputs and invoke a REST call. Callers
have the responsibility of handling the Requests libraries response object which can be None

"""


def report_get(api_key):
    pass


def report_list(api_key, page, per_page=30):

    url = "https://store.import.io/store/report/_search"

    querystring = {"_sort": "_meta.creationTimestamp",
                   "_page": page,
                   "_perpage": per_page,
                   "_apikey": api_key
                   }
    headers = {
        'accept': "*/*",
        'Cache-Control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()


def report_list_runs(api_key, guid, page, per_page=30):
    pass


def report_get_run(api_key, guid):
    pass


