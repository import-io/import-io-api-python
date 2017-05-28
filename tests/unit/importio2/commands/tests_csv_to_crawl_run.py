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
from ebayio import CsvToCrawlRun
from importio2 import CrawlRunAPI
from datetime import timedelta, datetime
import os

EXTRACTOR_ID = '5eeee942-09f3-4543-9695-cfa4408b5df6'
EXTRACTOR_ID_NEW = '922245f4-e277-410a-8fd3-bb9fb2d2922c'
CRAWL_RUN_ID = 'eb697a3c-f07b-468b-9b25-714c7057f055'
CSV_PATH = os.path.join(os.path.dirname(__file__), 'csv_to_json.csv')

FAILED_URL_COUNT = 0
SUCCESS_URL_COUNT = 3
TOTAL_URL_COUNT = 3
ROW_COUNT = 9
RUN_TIME = timedelta(minutes=5, seconds=5)
START_AT = datetime.now()
STOPPED_AT = START_AT + RUN_TIME


class TestCsvToCrawlRun(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_constructor(self):
        csv_to_crawl_run = CsvToCrawlRun()
        self.assertIsNotNone(csv_to_crawl_run)

    def test_csv_to_crawl_run(self):
        to_crawl = CsvToCrawlRun()
        to_crawl.run(crawl_run_id=CRAWL_RUN_ID, csv_path=CSV_PATH)

    def test_csv_to_crawl_run_new(self):
        api = CrawlRunAPI()
        crawl_run_id = api.create(extractor_id=EXTRACTOR_ID_NEW,
                                  failed_url_count=FAILED_URL_COUNT,
                                  success_url_count=SUCCESS_URL_COUNT,
                                  total_url_count=TOTAL_URL_COUNT,
                                  row_count=ROW_COUNT,
                                  started_at=START_AT,
                                  stopped_at=STOPPED_AT)

        to_crawl = CsvToCrawlRun()
        to_crawl.run(crawl_run_id, csv_path=CSV_PATH)
