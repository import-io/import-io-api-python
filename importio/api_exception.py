#
# Copyright 2016 BMC Software, Inc.
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
"""
Base exception class for pulse exceptions
"""

_product_name = 'Import.io'

logger = logging.getLogger(__name__)


class Error(Exception):
    """
    Base class for all API exceptions
    """
    def __init__(self):
        pass


class ConnectionError(Error):
    """
    Exception class for any network connection problems or errors
    """

    def __init__(self, error):
        super(ConnectionError, self).__init__()
        self.error = error

    def __str__(self):
        return "Error connecting to {0}: {1}".format(_product_name, self.error)


class HTTPResponseError(Error):
    """
    Indicates an HTTP response error when calling the API
    """
    def __init__(self, status_code, error):
        """
        Initialize exception with HTTP result code and error text
        :param status_code: HTTP Response code
        :param error: Text describing the error
        """
        super(HTTPResponseError, self).__init__()
        self.status_code = status_code
        self.error = error

    def __str__(self):
        """
        Converts to print friendly string
        :return: str
        """
        return "{0} API HTTP response of {1} : {2}".format(_product_name, self.status_code, self.error)
