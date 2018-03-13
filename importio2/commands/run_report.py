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

import json
import logging

import requests

from importio2 import CrawlRunAPI
from importio2 import ExtractorAPI
from importio2.commands import AdBase

logger = logging.getLogger(__name__)


class RunReport(AdBase):

    def __init__(self):
        super(RunReport, self).__init__()
        self._report_id = None
        self._diff_report = False
        self._data_report = False
        self._base_crawl_run_id = None
        self._compare_crawl_run_id = None

    def cli_description(self):
        return 'Generate a data or diff report'

    def handle_arguments(self):
        self._parser.add_argument('--base-crawl-run', action='store', dest='base_crawl_run_id',
                                  metavar='crawl_run_id', help='Base crawl run for the diff report')
        self._parser.add_argument('--compare-crawl-run', action='store', dest='compare_crawl_run_id',
                                  metavar='crawl_run_id', help='Comparison crawl run for the diff report')
        self._parser.add_argument('--report-id', action='store', dest='report_id',
                                  metavar='crawl_run_id', help='Identifier of the report to create')
        group = self._parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--diff', action='store_true', dest='diff_report', default=False,
                           help='Create a diff report')
        group.add_argument('--data', action='store_true', dest='data_report', default=False,
                           help='Create a data report')

        super(RunReport, self).handle_arguments()

    def get_arguments(self):
        super(RunReport, self).get_arguments()

        if self._args.diff_report:
            self._diff_report = self._args.diff_report
        if self._args.data_report is not None:
            self._data_report = self._args.data_report
        if self._args.report_id is not None:
            self._report_id = self._args.report_id

    def run(self, extractor_id, list=True, state=None):
        """
        Performs the operation as an API
        :param extractor_id: Identifier of the extractor
        :param list: Option to list
        :return:
        """
        pass

    def run_options(self):
        if self._data_report:
            self.create_data_report()
        elif self._diff_report:
            self.create_diff_report()

    def list_crawl_runs(self):
        api = ExtractorAPI()
        crawl_runs = api.get_crawl_runs(self._extractor_id)
        for cr in crawl_runs:
            fields = cr['fields']
            print("crawl_run_id: {0}, state: {1}".format(fields['guid'], fields['state']))

    def set_crawl_run_state(self, crawl_run_id, state):
        url = "https://store.import.io/{0}/{1}".format('crawlrun', crawl_run_id)
        data = {
            "state": state,
        }
        querystring = {
            "_apikey": self._api_key
        }
        headers = {
            'content-type': "application/json",
        }
        response = requests.request("PATCH", url, data=json.dumps(data), headers=headers, params=querystring)
        return response

    def disable_crawl_runs(self):
        cr_api = CrawlRunAPI()
        crawl_run = cr_api.get(self._crawl_run_id)
        extractor_id = crawl_run['extractorId']
        e_api = ExtractorAPI()
        crawl_runs = e_api.get_crawl_runs(extractor_id)
        for cr in crawl_runs:
            crawl_run_id = cr['fields']['guid']
            if self._crawl_run_id == crawl_run_id:
                continue
            self.set_crawl_run_state(crawl_run_id, 'CANCELLED')

    def create_data_report(self):
        url = "https://api.import.io/report/{0}/run".format(self._report_id)
        querystring = {
            "_apikey": self._api_key
        }
        response = requests.request("POST", url, params=querystring)
        print(response.text)
        return response

    def create_diff_report(self):
        pass

    def execute(self):
        """
        Performs the operation as a CLI
        :return:
        """
        logger.setLevel(logging.NOTSET)
        self.handle_arguments()
        self.run_options()


def main():
    """
    Entry point for the CLI
    :return: None
    """
    cli = RunReport()
    cli.execute()


if __name__ == '__main__':
    main()
