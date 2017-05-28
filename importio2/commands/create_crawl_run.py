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

from importio2.commands import AdBase
from importio2 import CrawlRunAPI
from datetime import datetime
from dateutil.parser import parse
import logging

logger = logging.getLogger(__name__)

# - Inputs
#   * Extractor Id
#   * Fields needed to create a minimal Extractor
# - Outputs
#   * New Extractor
#   * Crawl Run Id


class CreateCrawlRun(AdBase):
    def __init__(self):
        super(CreateCrawlRun, self).__init__()
        self._failed_url_count = None
        self._success_url_count = None
        self._total_url_count = None
        self._row_count = None
        self._started_at = None
        self._stopped_at = None
        self._state = None

    def cli_description(self):
        return 'Creates a Crawl Run for an Extractor in the Object Store'

    def handle_arguments(self):
        """
        Handle the arguments specific to this CLI
        :return: None
        """

        self.add_extractor_id_arg()
        self._parser.add_argument('--failed-url-count', action='store', dest='failed_url_count', type=int,
                                  metavar='count', required=True, help='Number of failed URLs')
        self._parser.add_argument('--success-url-count', action='store', dest='success_url_count', type=int,
                                  metavar='count', required=True, help='Number of successful URLs')
        self._parser.add_argument('--total-url-count', action='store', dest='total_url_count', type=int,
                                  metavar='count', required=True, help='Total Number of URLs')
        self._parser.add_argument('--row-count', action='store', dest='row_count', type=int,
                                  metavar='count', required=True, help='Number of rows returned')
        self._parser.add_argument('--started-at', action='store', dest='started_at',
                                  metavar='YY-mm-dd HH:MM:ss', required=True, help='Date and time crawl run started')
        self._parser.add_argument('--stopped-at', action='store', dest='stopped_at',
                                  metavar='YY-mm-dd HH:MM:ss', required=True, help='Date and time crawl run stopped')
        self._parser.add_argument('--state', action='store', dest='state', required=True,
                                  choices=['CANCELLED', 'FINISHED', 'PENDING', 'STARTED'],
                                  help='Sets the status of the crawl run')

        super(CreateCrawlRun, self).handle_arguments()
        self.get_arguments()

    def get_arguments(self):
        """
        Fetches the arguments from the arguments that have been parsed
        :return:
        """
        super(CreateCrawlRun, self).get_arguments()

        if 'failed_url_count' in self._args:
            self._failed_url_count = self._args.failed_url_count
        if 'success_url_count' in self._args:
            self._success_url_count = self._args.success_url_count
        if 'total_url_count' in self._args:
            self._total_url_count = self._args.total_url_count
        if 'row_count' in self._args:
            self._row_count = self._args.row_count
        if 'started_at' in self._args:
            try:
                self._started_at = int(self._args.started_at)
            except ValueError:
                self._started_at = self._args.started_at
        if 'stopped_at' in self._args:
            try:
                self._stopped_at = int(self._args.stopped_at)
            except ValueError:
                self._stopped_at = self._args.stopped_at
        if 'state' in self._args:
            self._state = self._args.state

        logger.info(
            "ARGS: id: {0}, failed: {1}, success: {2}, total: {3}, row: {4}, state: {5}, start: {6}, stop: {7}".format(
                self._extractor_id,
                self._failed_url_count,
                self._success_url_count,
                self._total_url_count,
                self._row_count,
                self._state,
                self._started_at,
                self._stopped_at
            ))
        # self._started_at, self._stopped_at = self._parse_dates(self._started_at, self._stopped_at)

    def _parse_dates(self, started_at, stopped_at):
        if isinstance(started_at, datetime):
            start_dt = int(started_at.strftime('%s')) * 1000
        elif isinstance(started_at, str):
            dt = parse(started_at)
            start_dt = int(dt.strftime('%s')) * 1000
        else:
            start_dt = started_at

        if isinstance(stopped_at, datetime):
            stop_dt = int(stopped_at.strftime('%s')) * 1000
        elif isinstance(stopped_at, str):
            dt = parse(stopped_at)
            stop_dt = int(dt.strftime('%s')) * 1000
        else:
            stop_dt = stopped_at

        return start_dt, stop_dt

    def run(self,
            extractor_id=None,
            success_url_count=None,
            total_url_count=None,
            row_count=None,
            started_at=None,
            stopped_at=None,
            api_key=None,
            failed_url_count=0,
            state='FINISHED'):

        if api_key is not None:
            self._api_key = api_key
        self._extractor_id = extractor_id
        self._failed_url_count = failed_url_count
        self._success_url_count = success_url_count
        self._total_url_count = total_url_count
        self._row_count = row_count
        self._started_at = started_at
        self._stopped_at = stopped_at
        self._state = state

        return self.create_crawl_run()

    def create_crawl_run(self):
        """
        Creates a crawl run with the provide parameters from the command line
        or run method
        :return: Crawl run id
        """
        api = CrawlRunAPI()
        logger.info(
            "RUN: id: {0}, failed: {1}, success: {2}, total: {3}, row: {4}, state: {5}, start: {6}, stop: {7}".format(
                self._extractor_id,
                self._failed_url_count,
                self._success_url_count,
                self._total_url_count,
                self._row_count,
                self._state,
                self._started_at,
                self._stopped_at
            ))

        crawl_run_id = api.create(
            extractor_id=self._extractor_id,
            failed_url_count=self._failed_url_count,
            success_url_count=self._success_url_count,
            total_url_count=self._total_url_count,
            row_count=self._row_count,
            started_at=self._started_at,
            stopped_at=self._stopped_at,
            state=self._state)

        return crawl_run_id

    def execute(self):
        """
        Main entry point to command line
        :return: Crawl Run Id
        """
        try:
            self.handle_arguments()
            print(self.create_crawl_run())
        except Exception as e:
            logger.exception(e)


def main():
    cli = CreateCrawlRun()
    cli.execute()


if __name__ == '__main__':
    main()
