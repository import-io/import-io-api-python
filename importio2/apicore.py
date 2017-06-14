#
# Copyright 2017 Import.io
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
import logging
import json

"""
Low-level REST API calls that specify the inputs and invoke a REST call. Callers
have the responsibility of handling the Requests libraries response object which can be None

"""

logger = logging.getLogger(__name__)


def extractor_get(api_key, guid):
    """
    Fetches the contents of an Extractor object from an account

    :param api_key: Import.io user API key
    :param guid: Extractor identifier
    :return: returns response object from requests library
    """

    url = "https://store.import.io/store/extractor/{0}".format(guid)

    querystring = {
        "_apikey": api_key
    }

    headers = {
        'cache-control': "no-cache",
    }
    logger.debug("url: {0}, headers: {1}, querystring: {2}".format(url, headers, querystring))

    return requests.request("GET", url, headers=headers, params=querystring)


def extractor_list(api_key, page):
    """
    Fetches the list of Extractors associated to an account

    :param api_key: Import.io user API key
    :param page: which page of the list to display
    :return: returns response object from requests library

    """

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
    logger.debug("url: {0}, headers: {1}, querystring: {2}".format(url, headers, querystring))

    return requests.request("GET", url, headers=headers, params=querystring)


def extractor_get_crawl_runs(api_key, guid, page, per_page):
    """

    :param api_key: Import.io user API key
    :param guid: Extractor identifier
    :param page: Specific crawl run page to display
    :param per_page: Number of crawl runs per page
    :return: returns response object from requests library
    """

    url = "https://store.import.io/store/crawlrun/_search"

    querystring = {"_sort": "_meta.creationTimestamp",
                   "_page": page,
                   "_perPage": per_page,
                   "extractorId": guid,
                   "_apikey": api_key
                   }
    headers = {
        'cache-control': "no-cache",
    }
    logger.debug("url: {0}, headers: {1}, querystring: {2}".format(url, headers, querystring))

    return requests.request("GET", url, headers=headers, params=querystring)


def extractor_query(api_key, guid, target_url):
    """
    Perform a live query with the extractor

    :param api_key: Import.io user API key
    :param guid: Extractor identifier
    :param target_url: URL to run the extractor against
    :return: Requests response object
    """

    url = "https://extraction.import.io/query/extractor/{0}".format(guid)

    querystring = {
        "_apikey": api_key,
        "url": target_url
    }

    headers = {
        'cache-control': "no-cache",
    }
    logger.debug("url: {0}, headers: {1}, querystring: {2}".format(url, headers, querystring))

    return requests.request("GET", url, headers=headers, params=querystring)


def extractor_url_list_get(api_key, guid, url_guid):
    """
    Gets the URL list associated with an extractor

    :param api_key: Import.io user API key
    :param guid: Extractor identifier
    :param url_guid: URL List identifier
    :return: Requests response object
    """

    url = "https://store.import.io/store/extractor/{0}/_attachment/urlList/{1}".format(guid, url_guid)

    querystring = {"_apikey": api_key}

    headers = {
        'accept-encoding': "gzip",
        'cache-control': "no-cache",
    }
    logger.debug("url: {0}, headers: {1}, querystring: {2}".format(url, headers, querystring))

    return requests.request("GET", url, headers=headers, params=querystring)


def extractor_url_list_put(api_key, guid, url_list):
    url = "https://store.import.io/store/extractor/{0}/_attachment/urlList".format(guid)

    querystring = {
        "_apikey": api_key
    }

    payload = url_list
    headers = {
        'content-type': "text/plain",
    }
    logger.debug("url: {0}, headers: {1}, querystring: {2}".format(url, headers, querystring))

    return requests.request("PUT", url, data=payload, headers=headers, params=querystring)


def extractor_cancel(api_key, guid):
    """
    Cancels a crawl run of an extractor

    :param api_key:
    :param api_key: Import.io user API key
    :param guid: Extractor identifier
    :return: Response object from requests REST call
    """

    url = "https://run.import.io/{0}/cancel".format(guid)

    querystring = {
        "_apikey": api_key
    }

    headers = {
        'cache-control': "no-cache",
    }
    logger.debug("url: {0}, headers: {1}, querystring: {2}".format(url, headers, querystring))

    return requests.request("POST", url, headers=headers, params=querystring)


def extractor_start(api_key, guid):
    """
    Initiates an crawl run of an extractor

    :param api_key: Import.io user API key
    :param guid: Extractor identifier
    :return: Response object from requests REST call
    """

    url = "https://run.import.io/{0}/start".format(guid)

    querystring = {
        "_apikey": api_key
    }

    headers = {
        'cache-control': "no-cache",
    }
    logger.debug("url: {0}, headers: {1}, querystring: {2}".format(url, headers, querystring))

    return requests.request("POST", url, headers=headers, params=querystring)


def extractor_csv(api_key, guid):
    """
    Returns the CSV file from the most recent extractor crawl run

    :param api_key: Import.io user API key
    :param guid: Extractor identifier
    :return: Response object from requests REST call
    """
    url = "https://data.import.io/extractor/{0}/csv/latest".format(guid)

    querystring = {
        '_apikey': api_key
    }

    headers = {
        'accept-encoding': "gzip",
        'cache-control': "no-cache",
    }
    logger.debug("url: {0}, headers: {1}, querystring: {2}".format(url, headers, querystring))

    return requests.request("GET", url, headers=headers, params=querystring)


def extractor_json(api_key, guid):
    url = "https://data.import.io/extractor/{0}/json/latest".format(guid)
    logger.debug("url: {0}".format(url))

    querystring = {
        "_apikey": api_key
    }

    headers = {
        'accept-encoding': "gzip",
        'cache-control': "no-cache",
    }
    logger.debug("url: {0}, headers: {1}, querystring: {2}".format(url, headers, querystring))

    return requests.request("GET", url, headers=headers, params=querystring)


def extractor_log(api_key, guid):

    url = "https://data.import.io/extractor/{0}/log/latest".format(guid)

    querystring = {
        "_apikey": api_key
    }

    headers = {
        'accept-encoding': "gzip",
    }
    logger.debug("url: {0}, headers: {1}, querystring: {2}".format(url, headers, querystring))

    return requests.request("GET", url, headers=headers, params=querystring)


def object_store_create(api_key, object_type, obj):
    url = "https://store.import.io/{0}".format(object_type)

    querystring = {
        "_apikey": api_key
    }

    payload = json.dumps(obj)
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'cache-control': "no-cache",
    }
    logger.debug("url: {0}, headers: {1}, querystring: {2}, payload: {3}".format(url, headers, querystring, payload))

    return requests.request("POST", url, data=payload, headers=headers, params=querystring)


def object_store_get(api_key, object_type, object_id):
    """
    Fetches an object of specific type from the Object Store
    :param api_key: Import.io API Key
    :param object_type: Type of object: crawlrun, extractor, etc
    :param object_id: Unique identifier of an object
    :return: response
    """
    url = "https://store.import.io/store/{0}/{1}".format(object_type, object_id)
    querystring = {
        "_apikey": api_key
    }
    headers = {
        'accept': "application/json",
        'cache-control': "no-cache",
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    return response


def object_store_put_attachment(api_key, object_type, object_id, attachment_field, attachment_contents,
                                attachment_type):
    url = "https://store.import.io/{0}/{1}/_attachment/{2}".format(object_type, object_id, attachment_field)

    querystring = {
        "_apikey": api_key
    }
    payload = attachment_contents
    headers = {
        'accept': "application/json",
        'content-type': attachment_type,
        'cache-control': "no-cache",
    }
    logger.debug("url: {0}, headers: {1}, querystring: {2}, payload: {3}".format(url, headers, querystring, payload))

    return requests.request("PUT", url, data=payload, headers=headers, params=querystring)


def object_store_change_ownership(api_key, object_type, object_id, owner_id):
    """
    Changes the ownership of an object (Extractor or Crawl Run) in the object store.
    NOTE: The API KEY must be from an account that has SUPPORT role
    :param api_key: Import.io API Key
    :param object_type: Specific object type
    :param object_id: Object Id of the Extractor or Crawl Run to change ownershipt
    :param owner_id: Owner GUID to set the objects ownership to.
    :return: response
    """

    url = "https://store.import.io/{0}/{1}".format(object_type, object_id)

    querystring = {"newOwner": owner_id,
                   "_apikey": api_key
                   }

    headers = {
    }

    response = requests.request("PATCH", url, headers=headers, params=querystring)

    return response
