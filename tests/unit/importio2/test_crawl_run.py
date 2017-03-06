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
from importio2 import CrawlRunAPI
from importio2 import ExtractorAPI

from tests.unit.importio2.test_data import CrawlRunCreateCrawlRun

EXTRACTOR_ID = ''


class TestExtractorAPI(TestCase):
    def test_constructor(self):
        api = CrawlRunAPI()
        self.assertIsNotNone(api)

    def test_create_crawl_run(self):
        crawl_run_api = CrawlRunAPI()
        crawl_run_id = crawl_run_api.create(
            extractor_id=CrawlRunCreateCrawlRun.EXTRACTOR_ID,
            failed_url_count=CrawlRunCreateCrawlRun.FAILED_URL_COUNT,
            success_url_count=CrawlRunCreateCrawlRun.SUCCESS_URL_COUNT,
            total_url_count=CrawlRunCreateCrawlRun.TOTAL_URL_COUNT,
            row_count=CrawlRunCreateCrawlRun.ROW_COUNT,
            started_at=CrawlRunCreateCrawlRun.STARTED_AT,
            stopped_at=CrawlRunCreateCrawlRun.STOPPED_AT)

        self.assertIsNotNone(crawl_run_id)

        extractor_api = ExtractorAPI()
        crawl_run = extractor_api.get_crawl_runs(EXTRACTOR_ID)
        run = crawl_run[0]
        self.assertIsNotNone(run)
        self.assertEqual(crawl_run_id, run['_id'])
        self.assertEqual('CrawlRun', run['_type'])
        fields = run['fields']
        self.assertEqual(CrawlRunCreateCrawlRun.EXTRACTOR_ID, fields['extractorId'])
        self.assertEqual(CrawlRunCreateCrawlRun.STATE, fields['state'])
        self.assertEqual(CrawlRunCreateCrawlRun.SUCCESS_URL_COUNT, fields['successUrlCount'])
        self.assertEqual(CrawlRunCreateCrawlRun.TOTAL_URL_COUNT, fields['totalUrlCount'])
        self.assertEqual(CrawlRunCreateCrawlRun.FAILED_URL_COUNT, fields['failedUrlCount'])
        self.assertEqual(CrawlRunCreateCrawlRun.ROW_COUNT, fields['rowCount'])
        self.assertEqual(CrawlRunCreateCrawlRun.STOPPED_AT, fields['stoppedAt'])
        self.assertEqual(CrawlRunCreateCrawlRun.STARTED_AT, fields['startedAt'])

    def test_json_attachment(self):
        crawl_run_api = CrawlRunAPI()

