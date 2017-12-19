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
from importio2.commands import AdBase
import requests

# - Inputs
#   * Extractor Id
#   * Crawl Run Id (optional)
#   * Output directory
# - Outputs
#   * File in file system


class CsvDownload(AdBase):

    def __init__(self):
        super(CsvDownload, self).__init__()
        self._csv_id = None

    def cli_description(self):
        """
        Provides the description of what operation this CLI performs
        :return: Description of the CLI's operation
        """
        return 'Downloads a CSV from an Extractor to a local file system'

    def get_arguments(self):
        """
        Returns the required arguments after they are processed by handle_arguments
        :return:
        """
        super(CsvDownload, self).get_arguments()

    def handle_arguments(self):
        self.add_crawl_run_id_arg()
        self.add_file_output_path_arg()
        super(CsvDownload, self).handle_arguments()

    def run(self,
            crawl_run_id,
            csv_id,
            output_path,
            api_key=None):
        """
        Executes the CLIs operation which is to down load a CSV file from an extractor
        :param crawl_run_id: Identifies which of the crawls to extract from the Extractors crawl runs
        :param csv_id: CSV file attachment id
        :param output_path: Path to write the CSV file in the local file system
        :param api_key: Import.io API Key from the account that has the extractor to download from
        :return: None
        """
        if api_key is not None:
            self._api_key = api_key
        self._crawl_run_id = crawl_run_id
        self._csv_id = csv_id
        self._output_path = output_path
        self.download_csv()

    def extractor_get_csv(self):
        """
        Returns the contents of the crawl run from an extractor.
        :return:
        """
        url = "https://data.import.io/crawlrun/{0}/_attachment/csv/{0}".format(self._extractor_id, self._csv_id)

        querystring = {
            "_apikey": self._api_key
        }

        headers = {
            'accept-encoding': "gzip",
            'cache-control': "no-cache",
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        response.raise_for_status()

        return response

    def download_csv(self):
        """
        Calls the member function to get the CSV file contents and
        then writes to a file
        :return: None
        """
        response = self.extractor_get_csv()
        with open(self._output_path, 'wt') as f:
            f.write(response.text)

    def execute(self):
        """
        Main entry point for the CLI
        :return: None
        """
        super(CsvDownload, self).execute()
        self.download_csv()


def main():
    cli = CsvDownload()
    cli.execute()


if __name__ == '__main__':
    main()
