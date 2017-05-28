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
import logging

logger = logging.getLogger(__name__)


class JsonToCrawlRun(AdBase):

    def __init__(self):
        super(JsonToCrawlRun, self).__init__()
        self._json_path = None
        self._crawl_run_id = None

    def cli_description(self):
        return 'Uploads a JSON file to a crawl run'

    def handle_arguments(self):
        self._parser.add_argument('--json-path', action='store', dest='json_path', metavar='path',
                                  required=True, help='Path to JSON file to upload to the crawl run')
        self._parser.add_argument('--crawl-run-id', action='store', dest='crawl_run_id', metavar='crawl_run_id',
                                  required=True, help='Specify crawl run id for replacing JSON')

        super(JsonToCrawlRun, self).handle_arguments()
        self.get_arguments()

    def get_arguments(self):
        super(JsonToCrawlRun, self).get_arguments()

        if 'json_path' in self._args:
            self._json_path = self._args.json_path

        if 'crawl_run_id':
            self._crawl_run_id = self._args.crawl_run_id

    def json_to_crawl_run(self):
        """
        Peforms the operation to add a JSON document to an existing crawl run
        :return:  None
        """
        api = CrawlRunAPI()
        api.json_attachment(crawl_run_id=self._crawl_run_id, contents=self._json_path)

    def run(self, crawl_run_id, json_path):
        """
        Performs the operation as an API
        :param crawl_run_id: crawl run id of existing crawl run
        :param json_path: Path to the JSON document to upload
        :return:
        """
        self._crawl_run_id = crawl_run_id
        self._json_path = json_path
        self.json_to_crawl_run()

    def execute(self):
        """
        Performs the operation as a CLI
        :return:
        """
        self.handle_arguments()
        self.json_to_crawl_run()


def main():
    """
    Entry point for the CLI
    :return: None
    """
    cli = JsonToCrawlRun()
    cli.execute()

if __name__ == '__main__':
    main()