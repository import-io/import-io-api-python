#
# Copyright 2016 Import.io
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

import requests

#
# Extractor
#


def extractor_get(api_key, extractor_id):

    url = "https://store.import.io/store/extractor/{0}".format(extractor_id)

    querystring = {
        "_apikey": api_key
    }

    headers = {
        'cache-control': "no-cache",
    }

    return requests.request("GET", url, headers=headers, params=querystring)


def extractor_list(api_key, page):

    url = "https://store.import.io/store/extractor/_search"

    querystring = {"_sort": "_meta.creationTimestamp",
                   "_mine": "true",
                   "q": "_missing_%3Aarchived%20OR%20archived%3Afalse",
                   "_page": page,
                   "_apikey": api_key
                   }

    headers = {
        'cache-control': "no-cache",
    }

    return requests.request("GET", url, headers=headers, params=querystring)


def extractor_get_crawl_runs(api_key, extractor_id, page, per_page):

    url = "https://store.import.io/store/crawlrun/_search"

    querystring = {"_sort": "_meta.creationTimestamp",
                   "_page": page,
                   "_perPage": per_page,
                   "extractorId": extractor_id,
                   "_apikey": api_key
                   }
    headers = {
        'cache-control': "no-cache",
    }

    return requests.request("GET", url, headers=headers, params=querystring)
