#!/usr/bin/env python
#
# Copyright 2018 Import.io
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
import csv
import logging
from importio2.commands import AdBase


class DownloadCrawlRunData(AdBase):

    def __init__(self):
        super(DownloadCrawlRunData, self).__init__()

    def cli_description(self):
        """
        Provides the description of what operation this CLI performs
        :return: Description of the CLI's operation
        """
        return 'Downloads all the extract data from an account'

    def get_arguments(self):
        """
        Returns the required arguments after they are processed by handle_arguments
        :return:
        """
        super(DownloadCrawlRunData, self).get_arguments()

    def handle_arguments(self):
        super(DownloadCrawlRunData, self).handle_arguments()

        self._parser.add_argument('-l', '--list', action='store_true', dest='list',
                                  help='List the extractors in an account')

    def do_list_extractors(self):
        pass

    def run(self, api_key=None):
        """
        Executes the CLIs operation which is to get the statistics of all Extractors/Crawl Runs
        :param api_key: Import.io API Key from the account that has the extractor to download from
        :return: None
        """
        if api_key is not None:
            self._api_key = api_key

    def execute(self):
        """
        Main entry point for the CLI
        :return: None
        """
        super(DownloadCrawlRunData, self).execute()
        logging.basicConfig(level=logging.ERROR)

        if self._list:
            self.do_list_extractors()
        if self._dump:
            self.do_dump()


def main():
    cli = DownloadCrawlRunData()
    cli.execute()


if __name__ == '__main__':
    main()
