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
from datetime import datetime
import requests

from importio2 import ExtractorAPI
from importio2.commands import AdBase

logger = logging.getLogger(__name__)


class CrawlRunStatus(AdBase):

    def __init__(self):
        super(CrawlRunStatus, self).__init__()
        self._all = False
        self._list = False
        self._state = None

    def cli_description(self):
        return 'Gets or sets the state of crawl runs'

    def handle_arguments(self):
        self.add_extractor_id_arg(required=False)
        self.add_crawl_run_id_arg(required=False)
        self._parser.add_argument('-a', '--all', action='store_true', dest='all', default=False,
                                  help='Sets the state on ALL of the crawlruns')
        group = self._parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-l', '--list', action='store_true', dest='list', default=False,
                           help='List the crawl runs and their status of and extractor')
        group.add_argument('-s', '--state', action='store', dest='state',
                           choices=['CANCELLED', 'FAILED', 'FINISHED', 'PENDING', 'STARTED'],
                           help='State to set crawlrun')

        super(CrawlRunStatus, self).handle_arguments()

    def get_arguments(self):
        super(CrawlRunStatus, self).get_arguments()

        if self._args.list:
            self._list = self._args.list

        if self._args.state is not None:
            self._state = self._args.state

        if self._args.all:
            self._all = self._args.all

    def run(self, extractor_id, list=True, state=None):
        """
        Performs the operation as an API
        :param extractor_id: Identifier of the extractor
        :param list: Option to list
        :return:
        """
        self._list = list
        self._state = state

    def set_all_crawl_run_states(self):
        api = ExtractorAPI()
        crawl_runs = api.get_crawl_runs(self._extractor_id)
        for cr in crawl_runs:
            guid = cr['fields']['guid']
            self._crawl_run_id = guid
            self.set_crawl_run_state()

    def run_options(self):
        if self._list:
            self.list_crawl_runs()
        elif self._all and self._state is not None:
            self.set_all_crawl_run_states()
        elif self._state is not None:
            self.set_crawl_run_state()

    def list_crawl_runs(self):
        api = ExtractorAPI()
        crawl_runs = api.get_crawl_runs(self._extractor_id)
        for cr in crawl_runs:
            fields = cr['fields']
            meta = fields['_meta']
            created_ts = meta['creationTimestamp']
            created_dt = datetime.fromtimestamp(created_ts/1000)
            print("crawl_run_id: {0}, state: {1}, created: {2}".format(fields['guid'], fields['state'], created_dt))

    def set_crawl_run_state(self):
        url = "https://store.import.io/{0}/{1}".format('crawlrun', self._crawl_run_id)
        data = {
            "state": self._state,
        }
        querystring = {
            "_apikey": self._api_key
        }
        headers = {
            'content-type': "application/json",
        }
        response = requests.request("PATCH", url, data=json.dumps(data), headers=headers, params=querystring)
        return response

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
    cli = CrawlRunStatus()
    cli.execute()


if __name__ == '__main__':
    main()
