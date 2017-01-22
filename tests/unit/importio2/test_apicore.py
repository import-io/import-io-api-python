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
from importio2.apicore import extractor_cancel
from importio2.apicore import extractor_csv
from importio2.apicore import extractor_json
from importio2.apicore import extractor_get
from importio2.apicore import extractor_query
from importio2.apicore import extractor_start
from importio2.apicore import extractor_url_list_get
from importio2.apicore import extractor_get_crawl_runs

from tests.unit.importio2.test_data import ExtractorCSVTestData
from tests.unit.importio2.test_data import ExtractorJSONTestData
from tests.unit.importio2.test_data import ExtractorCrawlRunsTestData
import requests
import json
import logging

#logging.basicConfig(level=logging.DEBUG)

# Todo: Refactor standard location for test data
EXTRACTOR_GUID = 'a3fcec06-08b4-4b96-8fa8-a942f99cd1aa'
EXTRACTOR_URL_LIST_GUID = '12834ceb-76d2-4072-98bb-7e41a7c032ae'
EXTRACTOR_QUERY_URL = u'http://www.example.com/'
EXTRACTOR_NAME = 'API_TEST-example.com'
EXTRACTOR_RUNTIME_CONFIG = 'b8debacc-b50d-46ce-a666-a1fb20420792'

API_TEST_GET_URL_LIST = '9dd8b560-70c1-43f1-902d-567ac2e2cf3f'
API_TEST_GET_URL_LIST_GUID = '0c5ee717-b9b9-4023-811d-e6ee5cf11ce9'

API_TEST_START_CANCEL = 'df761a66-c218-46ab-9655-01250e9c7214'


class TestApiCore(TestCase):

    def setUp(self):
        self._api_key = os.environ['IMPORT_IO_API_KEY']
        self._response = extractor_get(self._api_key, EXTRACTOR_GUID)
        self._extractor = json.loads(self._response.text)

    def test_extractor_get(self):
        response = extractor_get(self._api_key, EXTRACTOR_GUID)
        self.assertEquals(response.status_code, requests.codes.ok)

    def test_extractor_id(self):
        self.assertEquals(self._extractor['guid'], EXTRACTOR_GUID)

    def test_extractor_name(self):
        self.assertEquals(self._extractor['name'], EXTRACTOR_NAME)

    def test_extractor_url_list_get(self):
        response = extractor_url_list_get(self._api_key, EXTRACTOR_GUID, EXTRACTOR_URL_LIST_GUID)

    def test_extractor_url_list_get_long(self):
        response = extractor_url_list_get(self._api_key, API_TEST_GET_URL_LIST, API_TEST_GET_URL_LIST_GUID)
        self.assertEqual(requests.codes.OK, response.status_code)
        content = """http://www.ikea.com/us/en/search/?query=chairs&pageNumber=1
http://www.ikea.com/us/en/search/?query=chairs&pageNumber=2
http://www.ikea.com/us/en/search/?query=chairs&pageNumber=3
http://www.ikea.com/us/en/search/?query=chairs&pageNumber=4
http://www.ikea.com/us/en/search/?query=chairs&pageNumber=5
http://www.ikea.com/us/en/search/?query=chairs&pageNumber=6
http://www.ikea.com/us/en/search/?query=chairs&pageNumber=7
http://www.ikea.com/us/en/search/?query=chairs&pageNumber=8
http://www.ikea.com/us/en/search/?query=chairs&pageNumber=9
http://www.ikea.com/us/en/search/?query=chairs&pageNumber=10"""
        self.assertEqual(content, response.text)

    def test_extractor_query(self):
        response = extractor_query(self._api_key, EXTRACTOR_GUID, EXTRACTOR_QUERY_URL)
        self.assertEqual(requests.codes.OK, response.status_code)
        result = response.json()
        extractor_data = result['extractorData']
        data = extractor_data['data']
        page_data = result['pageData']

        self.assertEqual(-1, result['sequenceNumber'])
        self.assertEqual(EXTRACTOR_QUERY_URL, result['url'])
        self.assertEqual(requests.codes.OK, page_data['statusCode'])
        self.assertEqual(EXTRACTOR_QUERY_URL, result['url'])
        self.assertEqual(EXTRACTOR_RUNTIME_CONFIG, result['runtimeConfigId'])

    def test_extractor_get_crawl_runs(self):
        response = extractor_get_crawl_runs(self._api_key, ExtractorCrawlRunsTestData.EXTRACTOR_ID, 1, 30)
        self.assertEqual(requests.codes.OK, response.status_code)
        result = response.json()

        hits = result['hits']['hits']
        self.assertEqual(ExtractorCrawlRunsTestData.CRAWL_RUNS_LEN, len(hits))
        crawl_run = hits[0]
        crawl_run_fields = crawl_run['fields']

        self.assertEqual(ExtractorCrawlRunsTestData.GUID, crawl_run_fields['guid'])
        self.assertEqual(ExtractorCrawlRunsTestData.TYPE, crawl_run['_type'])
        self.assertEqual(ExtractorCrawlRunsTestData.GUID, crawl_run['_id'])
        self.assertEqual(ExtractorCrawlRunsTestData.EXTRACTOR_ID, crawl_run_fields['extractorId'])
        self.assertEqual(ExtractorCrawlRunsTestData.STATE, crawl_run_fields['state'])
        self.assertEqual(ExtractorCrawlRunsTestData.TOTAL_URL_COUNT, crawl_run_fields['totalUrlCount'])
        self.assertEqual(ExtractorCrawlRunsTestData.SUCCESS_URL_COUNT, crawl_run_fields['successUrlCount'])
        self.assertEqual(ExtractorCrawlRunsTestData.FAILED_URL_COUNT, crawl_run_fields['failedUrlCount'])

    def test_extractor_cancel(self):
        response = extractor_cancel(self._api_key, EXTRACTOR_GUID)
        self.assertEqual(requests.codes.BAD_REQUEST, response.status_code)

    def test_extractor_start(self):
        response = extractor_start(self._api_key, EXTRACTOR_GUID)
        self.assertEqual(requests.codes.OK, response.status_code)
        extractor_cancel(self._api_key, EXTRACTOR_GUID)

    def test_extractor_start_cancel(self):
        response = extractor_start(self._api_key, API_TEST_START_CANCEL)
        self.assertEqual(requests.codes.OK, response.status_code)
        response = extractor_cancel(self._api_key, API_TEST_START_CANCEL)
        self.assertEqual(requests.codes.OK, response.status_code)

    def test_extractor_csv(self):
        response = extractor_csv(self._api_key, ExtractorCSVTestData.EXTRACTOR_ID)
        self.assertEqual(requests.codes.OK, response.status_code)
        results = response.text.split('\n')
        for r in results:
            print(r)
        self.assertEqual(ExtractorCSVTestData.CSV_LEN, len(results))

    def test_extractor_json(self):
        response = extractor_json(self._api_key, ExtractorJSONTestData.EXTRACTOR_ID)
        self.assertEqual(requests.codes.OK, response.status_code)
        results = response.text.split('\n')
        self.assertEqual(ExtractorJSONTestData.JSON_LEN, len(results))




