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
from importio2 import ExtractorAPI
from importio2.commands import CreateCrawlRun
from datetime import datetime
from time import sleep

EXTRACTOR_ID = '44201b13-6109-4620-b1f3-6435e5b202d8'
STARTED = int(datetime(2017, 12, 31, 1, 15, 30).timestamp()) * 1000
STOPPED = int(datetime(2017, 12, 31, 1, 15, 35).timestamp()) * 1000
STARTED_AT = datetime(2017, 12, 31, 1, 15, 30).strftime('%Y-%m-%d %H:%M:%S')
STOPPED_AT = datetime(2017, 12, 31, 1, 15, 35).strftime('%Y-%m-%d %H:%M:%S')
FAILED_URL_COUNT = 0
SUCCESS_URL_COUNT = 1
TOTAL_URL_COUNT = 1
ROW_COUNT = 2
STATE = 'FINISHED'


class TestCreateCrawlRun(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_run(self):
        crawl_run = CreateCrawlRun()
        crawl_run_id = crawl_run.run(extractor_id=EXTRACTOR_ID,
                                     failed_url_count=FAILED_URL_COUNT,
                                     success_url_count=SUCCESS_URL_COUNT,
                                     total_url_count=TOTAL_URL_COUNT,
                                     row_count=ROW_COUNT,
                                     started_at=STARTED_AT,
                                     stopped_at=STOPPED_AT,
                                     state='FINISHED')
        api = ExtractorAPI()
        sleep(5)
        crawl_run_list = api.get_crawl_runs(EXTRACTOR_ID)
        self.assertIsNotNone(crawl_run_list)
        run = crawl_run_list[0]
        self.assertIsNotNone(run)
        fields = run['fields']
        self.assertEqual(crawl_run_id, run['_id'])
        self.assertEqual(EXTRACTOR_ID, fields['extractorId'])
        self.assertEqual('FINISHED', fields['state'])
        self.assertEqual(STARTED, fields['startedAt'])
        self.assertEqual(STOPPED, fields['stoppedAt'])
        self.assertEqual(FAILED_URL_COUNT, fields['failedUrlCount'])
        self.assertEqual(SUCCESS_URL_COUNT, fields['successUrlCount'])
        self.assertEqual(TOTAL_URL_COUNT, fields['totalUrlCount'])
        self.assertEqual(ROW_COUNT, fields['rowCount'])
