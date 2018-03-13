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
import json
import logging
import sys

from importio2 import ExtractorAPI
from importio2.commands import AdBase

FIELD_NAMES = [
    "extractor_id",
    "extractor_name",
    "parent_extractor_id",
    "crawl_run_id",
    "create_dt",
    "modified_dt",
    "start_dt",
    "stopped_dt",
    "total_url_count",
    "success_url_count",
    "failed_url_count",
    "row_count",
    "state",
    "url_list_id",
    "json",
    "log",
    "sample",
    "csv"
]


class AccountStats(AdBase):

    def __init__(self):
        self._command = None
        self._count = None
        self._full_dump = None
        self._list = None
        self._monitor = None
        self._output_file = None
        super(AccountStats, self).__init__()

    def cli_description(self):
        """
        Provides the description of what operation this CLI performs
        :return: Description of the CLI's operation
        """
        return 'Extracts data about the Extractors/Crawl Runs in an account'

    def get_arguments(self):
        """
        Returns the required arguments after they are processed by handle_arguments
        :return:
        """
        super(AccountStats, self).get_arguments()
        self._count = self._args.count
        self._full_dump = self._args.full_dump
        self._list = self._args.list
        self._monitor = self._args.monitor
        if self._output_path is not None:
            output_file = open(self._output_path, 'wt')
        else:
            output_file = sys.stdout
        self._output_file = csv.DictWriter(output_file, fieldnames=FIELD_NAMES)
        self._output_file.writeheader()

    def handle_arguments(self):
        self.add_file_output_path_arg(required=False)
        group = self._parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-c', '--count', action='store_true', dest='count', default=False,
                           help='Provide a count of the extractors in the account')

        group.add_argument('-f', '--full-dump', action='store_true', dest='full_dump', default=False,
                           help='Provide a full dump of crawl run meta data')
        group.add_argument('-l', '--list', action='store_true', dest='list', default=False,
                           help='Provide a list of the extractors in the account')
        group.add_argument('-m', '--monitor', action='store_true', dest='monitor', default=False,
                           help='Monitors each extractor and looks at each of the crawl runs')
        super(AccountStats, self).handle_arguments()

    def run(self, api_key=None):
        """
        Executes the CLIs operation which is to get the statistics of all Extractors/Crawl Runs
        :param api_key: Import.io API Key from the account that has the extractor to download from
        :return: None
        """
        if api_key is not None:
            self._api_key = api_key

    def do_count_extractors(self):
        api = ExtractorAPI()
        logging.basicConfig(level=logging.ERROR)
        extractor_list = api.list()
        print("Total Extractor: {0}".format(len(extractor_list)))

    def do_list_extractors(self):
        api = ExtractorAPI()
        logging.basicConfig(level=logging.ERROR)
        extractor_list = api.list()
        count = 0

        for extractor in extractor_list:
            count += 1
            #           if 'parentExtractorGuid' in extractor:
            extractor_data = json.dumps(extractor)
            print(extractor_data)
            name = extractor['fields']['name']
            print(name)
        print("extractor_count: {0}".format(count))

    def get_crawl_runs(self, guid):
        """
        Collects all the crawl meta data
        :param guid: Guid which identifies the extractor
        :return: None
        """
        api = ExtractorAPI()
        extractor = api.get(guid)
        extractor_name = extractor['name']
        if 'parentExtractorGuid' in extractor:
            parent_extractor_id = extractor['parentExtractorGuid']
        else:
            parent_extractor_id = None
        logging.basicConfig(level=logging.ERROR)
        crawl_run_list = api.get_crawl_runs(guid)
        for crawl_run in crawl_run_list:
            crawl_run_id = crawl_run['_id']
            fields = crawl_run['fields']
            modified_dt = fields['_meta']['timestamp']
            create_dt = fields['_meta']['creationTimestamp']
            state = fields['state']
            if 'startedAt' in fields:
                start_dt = fields['startedAt']
            else:
                start_dt = None
            if 'stoppedAt' in fields:
                stop_dt = fields['stoppedAt']
            else:
                stop_dt = None
            if 'totalUrlCount' in fields:
                total_url_count = fields['totalUrlCount']
            else:
                total_url_count = None
            if 'successUrlCount' in fields:
                success_url_count = fields['successUrlCount']
            else:
                success_url_count = None
            if 'failedUrlCount' in fields:
                failed_url_count = fields['failedUrlCount']
            else:
                failed_url_count = None
            if 'rowCount' in fields:
                row_count = fields['rowCount']
            else:
                row_count = None
            if 'urlListId' in fields:
                url_list_id = fields['urlListId']
            else:
                url_list_id = None
            if 'json' in fields:
                json_attach = fields['json']
            else:
                json_attach = None
            if 'csv' in fields:
                csv_attach = fields['csv']
            else:
                csv_attach = None
            if 'log' in fields:
                log_attach = fields['log']
            else:
                log_attach = None
            if 'sample' in fields:
                sample_attach = fields['sample']
            else:
                sample_attach = None
            d = {
                "extractor_id": guid,
                "extractor_name": extractor_name,
                "parent_extractor_id": parent_extractor_id,
                "crawl_run_id": crawl_run_id,
                "create_dt": create_dt,
                "modified_dt": modified_dt,
                "start_dt": start_dt,
                "stopped_dt": stop_dt,
                "total_url_count": total_url_count,
                "success_url_count": success_url_count,
                "failed_url_count": failed_url_count,
                "row_count": row_count,
                "state": state,
                "url_list_id": url_list_id,
                "json": json_attach,
                "csv": csv_attach,
                "log": log_attach,
                "sample": sample_attach
            }
            self._output_file.writerow(d)

    def do_dump(self):
        api = ExtractorAPI()
        extractor_list = api.list()
        for extractor in extractor_list:
            guid = extractor['_id']
            self.get_crawl_runs(guid)

    def execute(self):
        """
        Main entry point for the CLI
        :return: None
        """
        super(AccountStats, self).execute()
        logging.basicConfig(level=logging.ERROR)

        if self._count:
            self.do_count_extractors()
        if self._list:
            self.do_list_extractors()
        if self._full_dump:
            self.do_dump()


def main():
    cli = AccountStats()
    cli.execute()


if __name__ == '__main__':
    main()
