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

import re
import os
import hashlib
import json

from unittest import TestCase
import tempfile
from importio2 import Extractor
from importio2 import ExtractorAPI

from tests.unit.importio2.test_data import ExtractorCSVTestData
from tests.unit.importio2.test_data import ExtractorJSONTestData
from tests.unit.importio2.test_data import ExtractorCrawlRunsTestData
from tests.unit.importio2.test_data import ExtractorCrawlRunStartTestData
from tests.unit.importio2.test_data import ExtractorQueryTestData
from tests.unit.importio2.test_data import ExtractorUrlListPutTestData
from tests.unit.importio2.test_data import ExtractorLogTestData
from tests.unit.importio2.test_data import ExtractorInteractiveTestData
import logging

logger = logging.getLogger(__name__)

API_TEST_GET_URL_LIST = '9dd8b560-70c1-43f1-902d-567ac2e2cf3f'
API_TEST_GET_URL_LIST_GUID = '0c5ee717-b9b9-4023-811d-e6ee5cf11ce9'

EXTRACTOR_GUID = 'a3fcec06-08b4-4b96-8fa8-a942f99cd1aa'
EXTRACTOR_NAME = 'API_TEST-example.com'

EXTRACTOR_TIMESTAMP = 1483577028065
EXTRACTOR_OWNER_GUID = '00a451ae-c38d-4752-a329-389b37cfc0aa'
EXTRACTOR_CREATOR_GUID = '00a451ae-c38d-4752-a329-389b37cfc0aa'
EXTRACTOR_LAST_EDITOR_GUID = 'd1100850-863b-4e0f-9fa0-5fbcd44db427'
EXTRACTOR_CREATION_TIMESTAMP = 1483576990715
EXTRACTOR_LATEST_CONFIG_ID = 'c7c4f78b-4b21-4d85-8e07-e0dbde9e517c'
EXTRACTOR_TRAINING = '77d32ed7-7e76-4860-b594-7c60d78ef1b9'
EXTRACTOR_URL_LIST = '12834ceb-76d2-4072-98bb-7e41a7c032ae'

EXTRACTOR_FIELD_0_ID = 'd5f64119-ec0f-4915-bb4d-83f28f83c622'
EXTRACTOR_FIELD_0_NAME = 'Description'
EXTRACTOR_FIELD_0_CAPTURE_LINK = False
EXTRACTOR_FIELD_0_TYPE = 'TEXT'

EXTRACTOR_FIELD_1_ID = 'db8ab2f7-465f-42bd-80ed-95701e99bb98'
EXTRACTOR_FIELD_1_NAME = 'Link'
EXTRACTOR_FIELD_1_CAPTURE_LINK = True
EXTRACTOR_FIELD_1_TYPE = 'TEXT'


class TestExtractorAPI(TestCase):

    def test_get_name(self):
        api = ExtractorAPI()
        name = api.get_name(EXTRACTOR_GUID)
        self.assertEqual(EXTRACTOR_NAME, name)

    def test_get_extractor(self):
        api = ExtractorAPI()
        extractor = api.get(EXTRACTOR_GUID)

        self.assertEqual(extractor['guid'], EXTRACTOR_GUID)
        self.assertEqual(extractor['name'], EXTRACTOR_NAME)
        self.assertEqual(extractor['_meta']['lastEditorGuid'], EXTRACTOR_LAST_EDITOR_GUID)
        self.assertEqual(extractor['_meta']['ownerGuid'], EXTRACTOR_OWNER_GUID)
        self.assertEqual(extractor['_meta']['creatorGuid'], EXTRACTOR_CREATOR_GUID)
        # Todo: Test to handle timestamp updating everytime the object is accessed
        # self.assertEqual(extractor['_meta']['timestamp'], EXTRACTOR_TIMESTAMP)
        self.assertEqual(extractor['_meta']['creationTimestamp'], EXTRACTOR_CREATION_TIMESTAMP)
        self.assertEqual(len(extractor['fields']), 2)

        self.assertEqual(extractor['fields'][0]['id'], EXTRACTOR_FIELD_0_ID)
        self.assertEqual(extractor['fields'][0]['name'], EXTRACTOR_FIELD_0_NAME)
        self.assertEqual(extractor['fields'][0]['captureLink'], EXTRACTOR_FIELD_0_CAPTURE_LINK)
        self.assertEqual(extractor['fields'][0]['type'], EXTRACTOR_FIELD_0_TYPE)

        self.assertEqual(extractor['fields'][1]['id'], EXTRACTOR_FIELD_1_ID)
        self.assertEqual(extractor['fields'][1]['name'], EXTRACTOR_FIELD_1_NAME)
        self.assertEqual(extractor['fields'][1]['captureLink'], EXTRACTOR_FIELD_1_CAPTURE_LINK)
        self.assertEqual(extractor['fields'][1]['type'], EXTRACTOR_FIELD_1_TYPE)

        self.assertEqual(extractor['latestConfigId'], EXTRACTOR_LATEST_CONFIG_ID)
        self.assertEqual(extractor['training'], EXTRACTOR_TRAINING)
        # self.assertEqual(extractor['urlList'], EXTRACTOR_URL_LIST)

    def test_url_list_get(self):
        api = ExtractorAPI()
        url_list = api.get_url_list(API_TEST_GET_URL_LIST)
        self.assertEqual(10, len(url_list))

    def test_url_list_put(self):
        api = ExtractorAPI()
        url_list = ExtractorUrlListPutTestData.EXTRACTOR_ID.split('\n')
        url_id = api.put_url_list(ExtractorUrlListPutTestData.EXTRACTOR_ID, url_list)
        self.assertIsNotNone(re.match(r'[0-9,a-f]{8}-[0-9,a-f]{4}-[0-9,a-f]{4}-[0-9,a-f]{4}-[0-9,a-f]{12}', url_id))

    def test_get_crawl_runs(self):
        api = ExtractorAPI()
        crawl_runs = api.get_crawl_runs(ExtractorCrawlRunsTestData.EXTRACTOR_ID)
        self.assertEqual(ExtractorCrawlRunsTestData.CRAWL_RUNS_LEN, len(crawl_runs))

        run = crawl_runs[0]
        run_fields = run['fields']
        self.assertEqual(ExtractorCrawlRunsTestData.GUID, run_fields['guid'])
        self.assertEqual(ExtractorCrawlRunsTestData.TYPE, run['_type'])
        self.assertEqual(ExtractorCrawlRunsTestData.GUID, run['_id'])
        self.assertEqual(ExtractorCrawlRunsTestData.EXTRACTOR_ID, run_fields['extractorId'])
        self.assertEqual(ExtractorCrawlRunsTestData.STATE, run_fields['state'])
        self.assertEqual(ExtractorCrawlRunsTestData.TOTAL_URL_COUNT, run_fields['totalUrlCount'])
        self.assertEqual(ExtractorCrawlRunsTestData.SUCCESS_URL_COUNT, run_fields['successUrlCount'])
        self.assertEqual(ExtractorCrawlRunsTestData.FAILED_URL_COUNT, run_fields['failedUrlCount'])

    def test_start(self):
        api = ExtractorAPI()
        crawl_run_id = api.start(ExtractorCrawlRunStartTestData.EXTRACTOR_ID)
        self.assertIsNotNone(crawl_run_id)

    def test_csv(self):
        api = ExtractorAPI()
        csv = api.csv(ExtractorCSVTestData.EXTRACTOR_ID)
        self.assertEqual(ExtractorCSVTestData.CSV_LEN, len(csv))

    def test_csv_to_path(self):
        api = ExtractorAPI()
        file = tempfile.NamedTemporaryFile(delete=False)
        api.csv(ExtractorCSVTestData.EXTRACTOR_ID, file.name)
        self.assertTrue(os.path.exists(file.name))
        with open(file.name) as f:
            lines = f.readlines()
            self.assertEqual(ExtractorCSVTestData.CSV_LEN, len(lines))

    def test_json(self):
        api = ExtractorAPI()
        result = api.json(ExtractorJSONTestData.EXTRACTOR_ID)
        self.assertEqual(ExtractorJSONTestData.JSON_LEN_API, len(result))

    def test_json_to_path(self):
        api = ExtractorAPI()
        file = tempfile.NamedTemporaryFile(delete=False)
        api.json(ExtractorJSONTestData.EXTRACTOR_ID, file.name)
        self.assertTrue(os.path.exists(file.name))
        with open(file.name) as f:
            reader = f.readlines()
            m = hashlib.md5()
            for line in reader:
                m.update(str.encode(line))
            self.assertEqual(b"'\xc1TN\x07\\\x0c\xbe\xfd\xc9i\xfdr\xd9\xd5\xd7", m.digest())

    def test_log_get(self):
        api = ExtractorAPI()
        result = api.log(ExtractorLogTestData.EXTRACTOR_ID)
        self.assertEqual(ExtractorLogTestData.LENGTH, len(result))

    def test_query(self):
        api = ExtractorAPI()
        result = api.query(ExtractorQueryTestData.EXTRACTOR_ID, ExtractorQueryTestData.PAGE_2_QUERY_URL)
        self.assertIsNotNone(result)
        self.assertEqual(ExtractorQueryTestData.PAGE_2_QUERY_URL, result['url'])
        group = result['extractorData']['data'][0]['group']
        self.assertIsNotNone(re.match(r'[A-Z]+', group[0]['product'][0]['text']))
        self.assertGreater(len(group[0]['description'][0]['text']), 0)
        self.assertIsNotNone(re.match(r'\$\d+\.\d{2}', group[0]['price'][0]['text']))


class TestExtractor(TestCase):
    def test_constructor_by_guid(self):
        extractor = Extractor(guid=EXTRACTOR_GUID)
        self.assertIsNotNone(extractor.guid, EXTRACTOR_GUID)

    def test_constructor_by_name(self):
        extractor = Extractor(name=EXTRACTOR_NAME)
        # self.assertIsNotNone(extractor.name, EXTRACTOR_NAME)

    def test_fields(self):
        extractor = Extractor(guid=EXTRACTOR_GUID)
        fields = extractor.fields
        self.assertEqual(2, len(fields))
        self.assertEqual(EXTRACTOR_FIELD_0_ID, fields[0].id)
        self.assertEqual(EXTRACTOR_FIELD_0_NAME, fields[0].name)
        self.assertEqual(EXTRACTOR_FIELD_0_CAPTURE_LINK, fields[0].capture_link)
        self.assertEqual(EXTRACTOR_FIELD_0_TYPE, fields[0].type)

        self.assertEqual(EXTRACTOR_FIELD_1_ID, fields[1].id)
        self.assertEqual(EXTRACTOR_FIELD_1_NAME, fields[1].name)
        self.assertEqual(EXTRACTOR_FIELD_1_CAPTURE_LINK, fields[1].capture_link)
        self.assertEqual(EXTRACTOR_FIELD_1_TYPE, fields[1].type)

    def test_url_list_get(self):
        extractor = Extractor(guid=API_TEST_GET_URL_LIST)
        self.assertEqual(10, len(extractor.url_list))

    def test_empty(self):
        try:
            extractor = Extractor()
            self.assertTrue(True)
        except ValueError:
            pass

    def test_extractor_start(self):
        extractor = Extractor(guid=EXTRACTOR_GUID)
        extractor.start()

    def test_extractor_csv(self):
        extractor = Extractor(guid=ExtractorCSVTestData.EXTRACTOR_ID)
        csv = extractor.csv()
        # Add one to account for the header which is stored separately in the CSVData instance
        self.assertEqual(ExtractorCSVTestData.CSV_LEN, len(csv) + 1)

    def test_extractor_json(self):
        extractor = Extractor(guid=ExtractorJSONTestData.EXTRACTOR_ID)
        json = extractor.json()
        self.assertEqual(ExtractorJSONTestData.JSON_ROWS, len(json))
        self.assertEqual('ï»¿url', json[0][0])
        self.assertEqual('Zip Codes', json[0][1])
        self.assertEqual('Link', json[0][2])

