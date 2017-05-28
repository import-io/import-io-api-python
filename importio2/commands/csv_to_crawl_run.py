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


class CsvToCrawlRun(AdBase):

    def __init__(self):
        super(CsvToCrawlRun, self).__init__()
        self._csv_path = None
        self._crawl_run_id = None

    def cli_description(self):
        return 'Uploads a CSV file to a crawl run'

    def handle_arguments(self):
        self._parser.add_argument('--csv-path', action='store', dest='csv_path', metavar='path',
                                  required=True, help='Path to CSV file to upload to the crawl run')
        self._parser.add_argument('--crawl-run-id', action='store', dest='crawl_run_id', metavar='crawl_run_id',
                                  required=True, help='Specify crawl run id for replacing CSV')

        super(CsvToCrawlRun, self).handle_arguments()
        self.get_arguments()

    def get_arguments(self):
        super(CsvToCrawlRun, self).get_arguments()

        if 'csv_path' in self._args:
            self._csv_path = self._args.csv_path

        if 'crawl_run_id':
            self._crawl_run_id = self._args.crawl_run_id

    def csv_to_crawl_run(self):
        """
        Peforms the operation to add a CSV file to an existing crawl run
        :return:  None
        """
        api = CrawlRunAPI()
        api.csv_attachment(crawl_run_id=self._crawl_run_id, contents=self._csv_path)

    def run(self, crawl_run_id, csv_path):
        """
        Performs the operation as an API
        :param crawl_run_id: crawl run id of existing crawl run
        :param csv_path: Path to the CSV file to upload
        :return:
        """
        self._crawl_run_id = crawl_run_id
        self._csv_path = csv_path
        self.csv_to_crawl_run()

    def execute(self):
        """
        Performs the operation as a CLI
        :return:
        """
        self.handle_arguments()
        self.csv_to_crawl_run()


def main():
    """
    Entry point for the CLI
    :return: None
    """
    cli = CsvToCrawlRun()
    cli.execute()

if __name__ == '__main__':
    main()