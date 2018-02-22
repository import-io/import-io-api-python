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

import json
import logging

import requests

"""
Low-level REST API calls that specify the inputs and invoke a REST call. Callers
have the responsibility of handling the Requests libraries response object which can be None

"""


def reports_list(api_key):

    url = "https://store.import.io/store/reportrun/_search"

    querystring = {"_sort": "_meta.creationTimestamp", "_page": "2", "_perpage": "30",
                   "_apikey": api_key
                   }

    headers = {
        'accept': "*/*",
        'Cache-Control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

