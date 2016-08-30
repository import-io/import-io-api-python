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

import json
import requests
import logging
import sys
from importio import HTTPResponseError
import six.moves.urllib.parse as urllib

logger = logging.getLogger(__name__)




def _handle_api_results(api_result, context=None):
    result = None
    # Only process if we get HTTP result of 200
    if api_result.status_code == requests.codes.ok:
        result = json.loads(api_result.text)
        return result


class ApiCall(object):
    def __init__(self, api_host=None, api_key=None):
        """
        :param api_host: api end point host
        :param api_key: Import.io :pi token
        :return: returns nothing

        :Example:

        from importio import API

        api = API(api_key='api.xxxxxxxxxx-yyyy')
        """
        self._kwargs = None
        self._methods = {"DELETE": self._do_delete,
                         "GET": self._do_get,
                         "PATCH": self._do_patch,
                         "POST": self._do_post,
                         "PUT": self._do_put}

        self._api_host = api_host
        self._api_key = api_key

        # All member variables related to REST CALL
        self._scheme = "https"
        self._method = "GET"
        self._headers = None
        self._data = None
        self._url = None
        self._path = None
        self._url_parameters = None

        self._api_result = None

    def _get_url_parameters(self):
        """
        Encode URL parameters
        """
        url_parameters = ''
        if self._url_parameters is not None:
            url_parameters = '?' + urllib.urlencode(self._url_parameters)
        return url_parameters

    def _do_get(self):
        """
        HTTP Get Request
        """
        return requests.get(self._url, data=self._data, headers=self._headers)

    def _do_delete(self):
        """
        HTTP Delete Request
        """
        return requests.delete(self._url, data=self._data, headers=self._headers)

    def _do_patch(self):
        """
        HTTP Patch Request
        """
        return requests.patch(self._url, data=self._data, headers=self._headers)

    def _do_post(self):
        """
        HTTP Post Request
        """
        return requests.post(self._url, data=self._data, headers=self._headers)

    def _do_put(self):
        """
        HTTP Put Request
        """
        return requests.put(self._url, data=self._data, headers=self._headers)

    def _good_response(status_code):
        """
        Determines what status codes represent a good response from an API call.
        """
        return status_code == requests.codes.ok

    def _form_url(self):
        return "{0}://{1}/{2}{3}".format(self._scheme, self._api_host, self._path, self._get_url_parameters())

    def _call_api(self, good_response):
        """
        Make an API call to get the metric definition
        """

        self._url = self._form_url()
        if self._headers is not None:
            logger.debug(self._headers)
        if self._data is not None:
            logger.debug(self._data)
        if len(self._get_url_parameters()) > 0:
            logger.debug(self._get_url_parameters())

        result = self._methods[self._method]()

        if not good_response(result.status_code):
            logger.error(self._url)
            logger.error(self._method)
            logger.error(self._headers)
            if self._data is not None:
                logger.error(self._data)
            logger.error(result)
            raise HTTPResponseError(result.status_code, result.text)
        self._api_result = result

    def _api_call(self, handle_results=_handle_api_results, good_response=_good_response, context=None):
        self._call_api(good_response=good_response)
        return handle_results(self._api_result, context)

