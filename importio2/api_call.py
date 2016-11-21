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
from importio2 import HTTPResponseError
import six.moves.urllib.parse as urllib

logger = logging.getLogger(__name__)


class ApiCall(object):
    """
    Implements the handling of HTTP(S) calls
    """

    def __init__(self, api_host=None, api_key=None):
        """
        :param api_host: api end point host
        :param api_key: Import.io :pi token
        :return: returns nothing

        :Example:

        from importio2 import API

        api = API(api_key='api.xxxxxxxxxx-yyyy')
        """
        self._kwargs = None
        self._methods = {"DELETE": self._do_delete,
                         "GET": self._do_get,
                         "PATCH": self._do_patch,
                         "POST": self._do_post,
                         "PUT": self._do_put}

        self.api_host = api_host
        self.api_key = api_key

        # All member variables related to REST CALL
        self.scheme = "https"
        self.method = "GET"
        self.headers = None
        self.auth = None
        self.data = None
        self.url = None
        self.path = None
        self.url_parameters = None
        self.fragment = None

        self.api_result = None

    def get_url_parameters(self):
        """
        Encode URL parameters from dictionary of name/value pairs
        """
        url_parameters = ''
        if self.url_parameters is not None:
            url_parameters = '?' + urllib.urlencode(self.url_parameters)
        return url_parameters

    def _do_get(self):
        """
        HTTP Get Request
        """
        return requests.get(self.url, data=self.data, headers=self.headers, auth=self.auth)

    def _do_delete(self):
        """
        HTTP Delete Request
        """
        return requests.delete(self.url, data=self.data, headers=self.headers, auth=self.auth)

    def _do_patch(self):
        """
        HTTP Patch Request
        """
        return requests.patch(self.url, data=self.data, headers=self.headers, auth=self.auth)

    def _do_post(self):
        """
        HTTP Post Request
        """
        return requests.post(self.url, data=self.data, headers=self.headers, auth=self.auth)

    def _do_put(self):
        """
        HTTP Put Request
        """
        return requests.put(self.url, data=self.data, headers=self.headers, auth=self.auth)

    def good_response(self):
        """
        Determines what status codes represent a good response from an API call.
        """
        return self.api_result.status_code == requests.codes.ok

    def get_url(self):
        """
        Generate URL specific for this API call
        :return:
        """
        self.url = "{0}://{1}/{2}{3}".format(self.scheme, self.api_host, self.path, self.get_url_parameters())

    def handle_api_results(self):
        """
        Translate the requests library result object to domain objects

        Classes that override this method are responsible for translating
        the requests library response object to Python objects
        :return:
        """
        result = None

        # Only process if we get HTTP result of 200
        if self.api_result.status_code == requests.codes.ok:
            result = json.loads(self.api_result.text)
            return result

    def api_request(self):
        """
        Low-level API for making a REST calls, callers are responsible for translating
        the request library request object
        """

        # Generate the URL
        self.get_url()

        # Log input parameters
        if self.headers is not None:
            logger.debug(self.headers)
        if self.data is not None:
            logger.debug(self.data)
        if len(self.get_url_parameters()) > 0:
            logger.debug(self.get_url_parameters())

        # Dispatch to the appropriate HTTP request method
        self.api_result = self._methods[self.method]()

        # Check for acceptable response, log error if
        # results not acceptable and raise exception
        if not self.good_response():
            logger.error(self.url)
            logger.error(self.method)
            logger.error(self.headers)
            if self.data is not None:
                logger.error(self.data)
            logger.error(self.api_result)
            raise HTTPResponseError(self.api_result.status_code, self.api_result.text)

    def api_call(self):
        """
        1) Issues the specific REST API call from the provide inputs
        2) Calls method to translate in the Python objects
        :return: Nore or objects generated by handle_api_results()
        """
        self.api_request()
        return self.handle_api_results()

