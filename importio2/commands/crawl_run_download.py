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
import argparse
import os
import sys
import requests
from importio2 import ExtractorAPI
from collections import UserList
from collections import UserDict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.ERROR)


class CrawlRun(UserDict):
    """
    Wrapper class to encapsulate Crawl Run
    """


class CrawlRunList(UserList):
    """
    Wrapper class for list of Crawl Runs
    """


class CrawlRunDown(object):
    def __init__(self):
        self._extractor_id = None
        self._output_dir = None
        self._format = None
        self._type = None
        self._crawl_run_ids = []
        self._api_key = os.environ['IMPORT_IO_API_KEY']
        self._crawl_run_list = CrawlRunList()

    def handle_arguments(self):
        """
        Process command line arguments
        :return:
        """
        parser = argparse.ArgumentParser(description='Downloads all of CSV/JSON files associated with an Extractor')
        parser.add_argument('-e', '--extractor-id', action='store', dest='extractor_id', metavar='id',
                            help='Extractor id identifying which extractor to download files from')
        parser.add_argument('-o', '--output-dir', action='store', dest='output_dir',
                            default=os.path.abspath(os.path.curdir), metavar='path',
                            required=False, help="Directory to download CSV/JSON files to")
        parser.add_argument('-t', '--type', action='store', dest='type', choices=['csv', 'json'], default='csv',
                            help='Selects the type of file to download. Default is CSV')
        parser.add_argument('-f', '--format', action='store', dest='format', default='%Y-%m-%d_%H_%M_%S',
                            help='Date format to use in the name of the output file.')

        args = parser.parse_args()

        if 'extractor_id' in args:
            self._extractor_id = args.extractor_id

        if 'output_dir' in args:
            self._output_dir = args.output_dir

        if 'type' in args:
            self._type = args.type

        if 'format' in args:
            self._format = args.format

        if self._type == 'json':
            print("JSON download not implemented", file=sys.stderr)
            sys.exit(1)

    def get_crawl_runs(self):
        """
        Calls the appropriate api to create a list of the crawl run ids associated with
        an Extractor
        :return:
        """

        url = "https://store.import.io/store/crawlrun/_search"

        querystring = {"_sort": "_meta.creationTimestamp",
                       "_page": "1",
                       "_perPage": "30",
                       "extractorId": self._extractor_id,
                       "_apikey": self._api_key,
                       }

        headers = {
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        d = response.json()

        data = d['hits']['hits']
        for r in data:
            crawl_run = CrawlRun(r)
            self._crawl_run_list.append(crawl_run)

    def generate_filename(self, crawl_run):
        api = ExtractorAPI()
        extractor = api.get(crawl_run['fields']['extractorId'])
        ts = datetime.fromtimestamp(int(crawl_run['fields']['stoppedAt']) / 1000).strftime(self._format)
        filename = "{filename}_{timestamp}.csv".format(filename=extractor['name'], timestamp=ts)

        return filename

    def download_csv(self, crawl_run):
        """
        Calls the API to download the CSV file from a crawl run
        :param crawl_run:
        :return: None
        """
        url = "https://store.import.io/store/crawlRun/{0}/_attachment/csv/{1}".format(crawl_run['_id'],
                                                                                      crawl_run['fields']['csv'])
        querystring = {
            "_apikey": self._api_key
        }

        headers = {
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        filename = self.generate_filename(crawl_run)

        path = os.path.join(self._output_dir, filename)
        logger.info("path: {0}".format(path))
        with open(path, 'wt') as f:
            # NOTE: Strip of the byte ordering by slicing
            f.write(response.text[3:])

    def download_json(self, crawl_run):
        pass

    def download_files(self):
        """
        Handles the downloading of files
        :return:
        """
        self.get_crawl_runs()

        for crawl_run in self._crawl_run_list:
            if crawl_run['fields']['state'] == 'FINISHED':
                if self._type == 'csv':
                    self.download_csv(crawl_run)
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
    cli = CrawlRunDown()
    cli.execute()


if __name__ == '__main__':
    main()
