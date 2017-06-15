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
import os
import importio2.apicore as apicore
import requests
import logging
from datetime import datetime
from dateutil import parser

logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)

CRAWL_RUN_OBJECT_TYPE = 'crawlrun'


class CrawlRunAPI(object):
    def __init__(self):
        self._api_key = os.environ['IMPORT_IO_API_KEY']

    @staticmethod
    def _parse_datetime(dt):
        if isinstance(dt, datetime):
            ts = int(dt.strftime('%s')) * 1000
        elif isinstance(dt, str):
            parsed = parser.parse(dt)
            ts = int(parsed.strftime('%s')) * 1000
        else:
            ts = dt
        return ts

    def change_ownership(self, crawl_run_id, owner_id):
        pass

    def create(self,
               extractor_id,
               failed_url_count,
               success_url_count,
               total_url_count,
               row_count,
               started_at,
               stopped_at,
               state='FINISHED'):
        """
        Creates a Crawl Run in an extractor
        :param extractor_id: Extractor to create the crawl run
        :param failed_url_count: Number of failed URLs in the run
        :param success_url_count: Number of Success URLs in the run
        :param total_url_count: Total number of URLs in the run
        :param row_count: Total rows returned by the run
        :param started_at: Time when run began
        :param stopped_at: Time when run finished
        :param state: Final state
        :return: crawl run id
        """
        data = {
            'extractorId': extractor_id,
            'failedUrlCount': failed_url_count,
            'successUrlCount': success_url_count,
            'totalUrlCount': total_url_count,
            'rowCount': row_count,
            'startedAt': CrawlRunAPI._parse_datetime(started_at),
            'stoppedAt': CrawlRunAPI._parse_datetime(stopped_at),
            'state': state
        }
        logger.info(
            "extractor_id: {0}, failed: {1}, success: {2}, total: {3}, row: {4}, state: {5}, start: {6}, stop: {7}".format(
                data['extractorId'],
                data['failedUrlCount'],
                data['successUrlCount'],
                data['totalUrlCount'],
                data['rowCount'],
                data['state'],
                data['startedAt'],
                data['stoppedAt']
            ))
        response = apicore.object_store_create(self._api_key, CRAWL_RUN_OBJECT_TYPE, data)
        response.raise_for_status()
        crawl_run_id = None
        if response.status_code == requests.codes.created:
            result = response.json()
            logger.info(result)
            crawl_run_id = result['guid']

        return crawl_run_id

    def get(self, crawl_run_id):
        """
        Retrieves a crawl run object from the Object Store
        :param crawl_run_id:
        :return: Dictionary representing a Crawl Run
        """
        response = apicore.object_store_get(api_key=self._api_key, object_type='crawlrun', object_id=crawl_run_id)
        result = None
        # Fetch the results only if a 200 codes returned
        if response.status_code == requests.codes.ok:
            result = response.json()
        return result

    def state(self, crawl_run_id):
        crawl_run = self.get(crawl_run_id)
        return crawl_run['state']

    def _attachment(self, crawl_run_id, object_type, contents, field, mime):
            if os.path.exists(contents):
                with open(contents) as f:
                    logger.info("Reading contents of: {0}".format(contents))
                    attachment_contents = f.read()
            else:
                attachment_contents = contents
            logger.info("attachment_contents: {0}".format(attachment_contents))
            response = apicore.object_store_put_attachment(self._api_key,
                                                           object_type,
                                                           crawl_run_id,
                                                           field,
                                                           attachment_contents.encode('utf-8'),
                                                           mime)

            attachment_id = None
            if response.status_code == requests.codes.ok:
                result = response.json()
                attachment_id = result['guid']

            return attachment_id

    def json_attachment(self, crawl_run_id, contents):

        return self._attachment(crawl_run_id=crawl_run_id, object_type='crawlrun', contents=contents,
                                field='json', mime='application/x-ldjson')

    def csv_attachment(self, crawl_run_id, contents):
        return self._attachment(crawl_run_id=crawl_run_id, object_type='crawlrun', contents=contents,
                                field='csv', mime='text/csv')

    def log_attachment(self, crawl_run_id, contents):
        return self._attachment(crawl_run_id=crawl_run_id, object_type='crawlrun', contents=contents,
                                field='csv', mime='text/csv')

