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

from unittest import TestCase
from importio2.commands import JsonToCrawlRun
from importio2 import CrawlRunAPI
from datetime import timedelta, datetime
import os

EXTRACTOR_ID = 'd4382ad6-b877-49b0-ac0e-20472cf43fe0'
EXTRACTOR_ID_NEW = 'ec820cf6-8561-4730-a8b7-fc2dafbd8541'
CRAWL_RUN_ID = 'd4382ad6-b877-49b0-ac0e-20472cf43fe0'
JSON_PATH = os.path.join(os.path.dirname(__file__), 'csv_to_json.json')

FAILED_URL_COUNT = 0
SUCCESS_URL_COUNT = 3
TOTAL_URL_COUNT = 3
ROW_COUNT = 9
RUN_TIME = timedelta(minutes=5, seconds=5)
START_AT = datetime.now()
STOPPED_AT = START_AT + RUN_TIME


class TestJsonToCrawlRUn(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_constructor(self):
        json_to_crawl_run = JsonToCrawlRun()
        self.assertIsNotNone(json_to_crawl_run)

    def test_json_to_crawl_run(self):
        to_crawl = JsonToCrawlRun()
        to_crawl.run(crawl_run_id=CRAWL_RUN_ID, json_path=JSON_PATH)

    def test_json_to_crawl_run_new(self):
        api = CrawlRunAPI()
        crawl_run_id = api.create(extractor_id=EXTRACTOR_ID_NEW,
                                  failed_url_count=FAILED_URL_COUNT,
                                  success_url_count=SUCCESS_URL_COUNT,
                                  total_url_count=TOTAL_URL_COUNT,
                                  row_count=ROW_COUNT,
                                  started_at=START_AT,
                                  stopped_at=STOPPED_AT)

        to_crawl = JsonToCrawlRun()
        to_crawl.run(crawl_run_id, json_path=JSON_PATH)



