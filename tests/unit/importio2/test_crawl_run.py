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
import os.path as path
import logging

from tests.unit.importio2.test_data import CrawlRunCreateCrawlRun
from tests.unit.importio2.test_data import CrawlRunJsonAttachment
from tests.unit.importio2.test_data import CrawlRunJsonAttachmentNew
from tests.unit.importio2.test_data import CrawlRunCsvAttachmentNew
from tests.unit.importio2.test_data import CrawlRunCsvJsonAttachment

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

EXTRACTOR_ID = ''

JSON_ATTACHMENT = """{"url":"http://www.example.com","result":{"extractorData":{"url":"http://www.example.com","resourceId":"f28ffcf17e9135b5fcd0913651304216","data":[{"group":[{"Description":[{"text":"This domain is established to be used for illustrative examples in documents. You may use this domain in examples without prior coordination or asking for permission."}]},{"Description":[{"text":"More information..."}],"Link":[{"text":"More information...","href":"http://www.iana.org/domains/example"}]}]}]},"pageData":{"resourceId":"f28ffcf17e9135b5fcd0913651304216","statusCode":200,"timestamp":1488760472551},"timestamp":1488761151967,"sequenceNumber":0}}"""


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
        crawl_run = extractor_api.get_crawl_runs(CrawlRunCreateCrawlRun.EXTRACTOR_ID)
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

    def test_json_attachment_existing(self):
        crawl_run_api = CrawlRunAPI()
        attachment_id = crawl_run_api.json_attachment(
            crawl_run_id=CrawlRunJsonAttachment.CRAWL_RUN_ID, contents=JSON_ATTACHMENT)

        extractor_api = ExtractorAPI()
        crawl_runs = extractor_api.get_crawl_runs(CrawlRunJsonAttachment.EXTRACTOR_ID)
        run = crawl_runs[0]
        fields = run['fields']
        self.assertIsNotNone(run)
        self.assertEqual(CrawlRunJsonAttachment.EXTRACTOR_ID, fields['extractorId'])
        self.assertEqual(CrawlRunJsonAttachment.TOTAL_URL_COUNT, fields['totalUrlCount'])
        self.assertEqual(CrawlRunJsonAttachment.SUCCESS_URL_COUNT, fields['successUrlCount'])
        self.assertEqual(CrawlRunJsonAttachment.FAILED_URL_COUNT, fields['failedUrlCount'])
        self.assertEqual(CrawlRunJsonAttachment.STATE, fields['state'])
        self.assertEqual(CrawlRunJsonAttachment.ROW_COUNT, fields['rowCount'])
        self.assertEqual(attachment_id, fields['json'])

    def test_json_attachment(self):
        crawl_run_api = CrawlRunAPI()
        json_path = path.abspath(path.join(path.dirname(__file__), CrawlRunJsonAttachmentNew.FILE_NAME))

        crawl_run_id = crawl_run_api.create(
            extractor_id=CrawlRunJsonAttachmentNew.EXTRACTOR_ID,
            failed_url_count=CrawlRunJsonAttachmentNew.FAILED_URL_COUNT,
            success_url_count=CrawlRunJsonAttachmentNew.SUCCESS_URL_COUNT,
            total_url_count=CrawlRunJsonAttachmentNew.TOTAL_URL_COUNT,
            row_count=CrawlRunJsonAttachmentNew.ROW_COUNT,
            started_at=CrawlRunJsonAttachmentNew.STARTED_AT,
            stopped_at=CrawlRunJsonAttachmentNew.STOPPED_AT)
        self.assertIsNotNone(crawl_run_id)
        logger.info("crawl_run_id: {0}".format(crawl_run_id))

        attachment_id = crawl_run_api.json_attachment(crawl_run_id=crawl_run_id, contents=json_path)
        extractor_api = ExtractorAPI()
        crawl_runs = extractor_api.get_crawl_runs(CrawlRunJsonAttachmentNew.EXTRACTOR_ID)
        run = crawl_runs[0]
        logger.info(run)
        fields = run['fields']
        self.assertIsNotNone(run)
        self.assertEqual(crawl_run_id, run['_id'])
        self.assertEqual(CrawlRunJsonAttachmentNew.STATE, fields['state'])
        self.assertEqual(CrawlRunJsonAttachmentNew.ROW_COUNT, fields['rowCount'])
        self.assertEqual(attachment_id, fields['json'])

    def test_csv_attachment(self):
        crawl_run_api = CrawlRunAPI()
        csv_path = path.abspath(path.join(path.dirname(__file__), CrawlRunCsvAttachmentNew.FILE_NAME))

        crawl_run_id = crawl_run_api.create(
            extractor_id=CrawlRunCsvAttachmentNew.EXTRACTOR_ID,
            failed_url_count=CrawlRunCsvAttachmentNew.FAILED_URL_COUNT,
            success_url_count=CrawlRunCsvAttachmentNew.SUCCESS_URL_COUNT,
            total_url_count=CrawlRunCsvAttachmentNew.TOTAL_URL_COUNT,
            row_count=CrawlRunCsvAttachmentNew.ROW_COUNT,
            started_at=CrawlRunCsvAttachmentNew.STARTED_AT,
            stopped_at=CrawlRunCsvAttachmentNew.STOPPED_AT)
        self.assertIsNotNone(crawl_run_id)
        logger.info("crawl_run_id: {0}".format(crawl_run_id))

        attachment_id = crawl_run_api.csv_attachment(crawl_run_id=crawl_run_id, contents=csv_path)

        extractor_api = ExtractorAPI()
        crawl_runs = extractor_api.get_crawl_runs(CrawlRunJsonAttachmentNew.EXTRACTOR_ID)
        run = crawl_runs[0]
        fields = run['fields']
        self.assertIsNotNone(run)
        self.assertEqual(crawl_run_id, run['_id'])
        self.assertEqual(CrawlRunCsvAttachmentNew.STATE, fields['state'])
        self.assertEqual(CrawlRunCsvAttachmentNew.ROW_COUNT, fields['rowCount'])
        self.assertEqual(attachment_id, fields['csv'])

    def test_csv_json_attachment(self):
        csv_path = path.abspath(path.join(path.dirname(__file__), CrawlRunCsvJsonAttachment.CSV_FILENAME))
        json_path = path.abspath(path.join(path.dirname(__file__), CrawlRunCsvJsonAttachment.JSON_FILENAME))
        crawl_run_api = CrawlRunAPI()
        csv_attachment_id = crawl_run_api.csv_attachment(
            crawl_run_id=CrawlRunCsvJsonAttachment.CRAWL_RUN_ID, contents=csv_path)
        json_attachment_id = crawl_run_api.json_attachment(
            crawl_run_id=CrawlRunCsvJsonAttachment.CRAWL_RUN_ID, contents=json_path)

        extractor_api = ExtractorAPI()
        crawl_runs = extractor_api.get_crawl_runs(CrawlRunCsvJsonAttachment.EXTRACTOR_ID)
        run = crawl_runs[0]
        fields = run['fields']
        self.assertIsNotNone(run)
        self.assertEqual(CrawlRunCsvJsonAttachment.EXTRACTOR_ID, fields['extractorId'])
        self.assertEqual(CrawlRunCsvJsonAttachment.TOTAL_URL_COUNT, fields['totalUrlCount'])
        self.assertEqual(CrawlRunCsvJsonAttachment.SUCCESS_URL_COUNT, fields['successUrlCount'])
        self.assertEqual(CrawlRunCsvJsonAttachment.FAILED_URL_COUNT, fields['failedUrlCount'])
        self.assertEqual(CrawlRunCsvJsonAttachment.STATE, fields['state'])
        self.assertEqual(CrawlRunCsvJsonAttachment.ROW_COUNT, fields['rowCount'])
        self.assertEqual(csv_attachment_id, fields['csv'])
        self.assertEqual(json_attachment_id, fields['json'])
