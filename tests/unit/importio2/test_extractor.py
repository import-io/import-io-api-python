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
EXTRACTOR_LAST_EDITOR_GUID = '00a451ae-c38d-4752-a329-389b37cfc0aa'
EXTRACTOR_CREATION_TIMESTAMP = 1483576990715
EXTRACTOR_LATEST_CONFIG_ID = 'b8debacc-b50d-46ce-a666-a1fb20420792'
EXTRACTOR_TRAINING = '77d32ed7-7e76-4860-b594-7c60d78ef1b9'
EXTRACTOR_URL_LIST = '12834ceb-76d2-4072-98bb-7e41a7c032ae'


class TestExtractorAPI(TestCase):

    def test_get_extractor(self):
        api = ExtractorAPI()
        extractor = api.get(EXTRACTOR_GUID)

        self.assertEqual(extractor['guid'], EXTRACTOR_GUID)
        self.assertEqual(extractor['name'], EXTRACTOR_NAME)
        self.assertEqual(extractor['_meta']['lastEditorGuid'], EXTRACTOR_LAST_EDITOR_GUID)
        self.assertEqual(extractor['_meta']['ownerGuid'], EXTRACTOR_OWNER_GUID)
        self.assertEqual(extractor['_meta']['creatorGuid'], EXTRACTOR_CREATOR_GUID)
        self.assertEqual(extractor['_meta']['timestamp'], EXTRACTOR_TIMESTAMP)
        self.assertEqual(extractor['_meta']['creationTimestamp'], EXTRACTOR_CREATION_TIMESTAMP)
        self.assertEqual(len(extractor['fields']), 2)

        self.assertEqual(extractor['fields'][0]['id'], 'd5f64119-ec0f-4915-bb4d-83f28f83c622')
        self.assertEqual(extractor['fields'][0]['name'], 'Description')
        self.assertEqual(extractor['fields'][0]['captureLink'], False)
        self.assertEqual(extractor['fields'][0]['type'], 'TEXT')

        self.assertEqual(extractor['fields'][1]['id'], 'db8ab2f7-465f-42bd-80ed-95701e99bb98')
        self.assertEqual(extractor['fields'][1]['name'], 'Link')
        self.assertEqual(extractor['fields'][1]['captureLink'], True)
        self.assertEqual(extractor['fields'][1]['type'], 'TEXT')

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
        pass

    def test_empty(self):
        try:
            extractor = Extractor()
            self.assertTrue(True)
        except ValueError:
            pass


