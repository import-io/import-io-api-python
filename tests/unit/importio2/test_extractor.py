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

from unittest import TestCase
from importio2 import Extractor
from importio2 import ExtractorAPI

EXTRACTOR_GUID = 'a3fcec06-08b4-4b96-8fa8-a942f99cd1aa'
EXTRACTOR_NAME = 'API_TEST-example.com'

EXTRACTOR_TIMESTAMP = 1483577028065
EXTRACTOR_OWNER_GUID = '00a451ae-c38d-4752-a329-389b37cfc0aa'
EXTRACTOR_CREATOR_GUID = '00a451ae-c38d-4752-a329-389b37cfc0aa'
EXTRACTOR_LAST_EDITOR_GUID = 'd1100850-863b-4e0f-9fa0-5fbcd44db427'
EXTRACTOR_CREATION_TIMESTAMP = 1483576990715
EXTRACTOR_LATEST_CONFIG_ID = 'b8debacc-b50d-46ce-a666-a1fb20420792'
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
        self.assertEqual(extractor['urlList'], EXTRACTOR_URL_LIST)


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

    def test_empty(self):
        try:
            extractor = Extractor()
            self.assertTrue(True)
        except ValueError:
            pass

    def test_extractor_start(self):
        extractor = Extractor(guid=EXTRACTOR_GUID)

        extractor.start()
