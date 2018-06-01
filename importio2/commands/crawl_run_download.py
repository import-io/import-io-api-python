#!/usr/bin/env python
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
import logging
import os
import sys
from collections import UserDict
from collections import UserList
from datetime import datetime

from importio2 import ExtractorAPI
from importio2 import CrawlRunAPI
from importio2.commands import AdBase

logger = logging.getLogger(__name__)


class CrawlRun(UserDict):
    """
    Wrapper class to encapsulate Crawl Run
    """


class CrawlRunList(UserList):
    """
    Wrapper class for list of Crawl Runs
    """


class CrawlRunDownload(AdBase):
    def __init__(self):
        super(CrawlRunDownload, self).__init__()
        self._extractor_id = None
        self._output_dir = None
        self._format = None
        self._type = None
        self._crawl_run_ids = []
        self._api_key = os.environ['IMPORT_IO_API_KEY']
        self._crawl_run_list = CrawlRunList()

    def cli_description(self):
        return 'Downloads all of CSV/JSON files associated with an Extractor'

    def handle_arguments(self):
        """
        Process command line arguments
        :return: None
        """
        self._parser.add_argument('-e', '--extractor-id', action='store', dest='extractor_id', metavar='id',
                                  required=True,
                                  help='Extractor id identifying which extractor to download files from')
        self._parser.add_argument('-o', '--output-dir', action='store', dest='output_dir',
                                  default=os.path.abspath(os.path.curdir), metavar='path',
                                  required=False, help="Directory to download CSV/JSON files to")
        self._parser.add_argument('-t', '--type', action='store', dest='type', choices=['csv', 'json'], default='csv',
                                  help='Selects the type of file to download. Default is CSV')
        self._parser.add_argument('-f', '--format', action='store', dest='format', default='%Y-%m-%d_%H_%M_%S',
                                  help='Date format to use in the name of the output file.')

        super(CrawlRunDownload, self).handle_arguments()

    def get_arguments(self):
        super(CrawlRunDownload)

        if self._args.extractor_id is not None:
            self._extractor_id = self._args.extractor_id

        if self._args.output_dir is not None:
            self._output_dir = self._args.output_dir

        if self._args.type is not None:
            self._type = self._args.type

        if self._args.format is not None:
            self._format = self._args.format

        if self._type == 'json':
            print("JSON download not implemented", file=sys.stderr)
            sys.exit(1)

    def get_crawl_runs(self):
        """
        Calls the appropriate api to create a list of the crawl run ids associated with
        an Extractor
        :return: List of crawl run objects
        """
        api = ExtractorAPI()
        return api.get_crawl_runs(self._extractor_id)

    def download_json(self, crawl_run_id):
        """
        Download the crawl in NDJSON.

        :param crawl_run_id:
        :return:
        """
        pass

    def download_csv(self, crawl_run_id):
        api = CrawlRunAPI()
        crawl_run = api.get(crawl_run_id)
        attachment_id = crawl_run['csv']

        timestamp = datetime.fromtimestamp(int(crawl_run['startedAt']) / 1000)

        path = os.path.join(self._output_dir, timestamp.strftime(self._format) + '.csv')
        logger.info(path)
        api.get_csv(crawl_run_id=crawl_run_id, file_id=attachment_id, path=path)

    def download_files(self):
        """
        Handles the downloading of files
        :return:
        """
        crawl_run_list = self.get_crawl_runs()

        for crawl_run in crawl_run_list:
            if crawl_run['fields']['state'] == 'FINISHED':
                crawl_run_id = crawl_run['_id']
                if self._type == 'csv':
                    self.download_csv(crawl_run_id)
                else:
                    self.download_json(crawl_run)

    def execute(self):
        """
        Main entry point for running this CLI
        :return:
        """
        self.handle_arguments()
        self.download_files()


def main():
    cli = CrawlRunDownload()
    cli.execute()


if __name__ == '__main__':
    main()
