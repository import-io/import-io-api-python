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
from __future__ import absolute_import

import os
from unittest import TestCase
from importio2.apicore import extractor_get
import requests
import json

EXTRACTOR_ID = 'a3fcec06-08b4-4b96-8fa8-a942f99cd1aa'
EXTRACTOR_NAME = 'API_TEST-example.com'


class TestApiCore(TestCase):

    def setUp(self):
        self._api_key = os.environ['IMPORT_IO_API_KEY']
        self._response = extractor_get(self._api_key, EXTRACTOR_ID)
        self._extractor = json.loads(self._response.text)

    def test_extractor_get(self):
        response = extractor_get(self._api_key, EXTRACTOR_ID)
        self.assertEquals(response.status_code, requests.codes.ok)

    def test_extractor_id(self):
        self.assertEquals(self._extractor['guid'], EXTRACTOR_ID)

    def test_extractor_id(self):
        self.assertEquals(self._extractor['name'], EXTRACTOR_NAME)


