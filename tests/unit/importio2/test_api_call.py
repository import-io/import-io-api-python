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
import logging
from unittest import TestCase
from importio2 import ApiCall
import json

logger = logging.getLogger(__name__)


class TestApiCall(TestCase):

    def setUp(self):
        self.api = ApiCall()

    def test_constructor(self):
        api = ApiCall()

    # def test_http_delete(self):
    #     self.api.api_host = 'httpbin.org'
    #     self.api.path = '/delete'
    #     request = self.api.api_request()
    #     self.assertEqual(request.status_code, 200)
    #
    #     d = json.loads(request.text)
    #     self.assertIsNotNone(d)

    def test_http_get(self):

        self.api.api_host = 'httpbin.org'
        self.api.scheme = 'http'
        self.api.path = "get"
        self.api.headers = {"Accept": "application/json"}

        self.api.api_request()

        self.assertEqual(self.api.api_result.status_code, 200)

        result = json.loads(self.api.api_result.text)
        self.assertIsNotNone(result)
        self.assertEqual('http://httpbin.org/get', result['url'])

    def test_http_patch(self):
        # self.assertFalse(True)
        pass

    def test_http_post(self):
        # self.assertFalse(True)
        pass
