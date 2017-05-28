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

    def cli_description(self):
        return 'Downloads a CSV from an Extractor to a local file system'

    def get_arguments(self):
        super(CsvDownload, self).get_arguments()

    def handle_arguments(self):
        self.add_extractor_id_arg()
        self.add_file_output_path_arg()

        self._args = self._parser.parse_args()

        self.get_arguments()

    def run(self,
            api_key=None,
            extractor_id=None,
            crawl_run_id=None,
            output_path=None):
        self._extractor_id = extractor_id
        if api_key is not None:
            self._api_key = api_key
        self._crawl_run_id = crawl_run_id
        self._output_path = output_path
        self.download_csv()

    def extractor_get_csv(self):
        url = "https://data.import.io/extractor/{0}/csv/latest".format(self._extractor_id)

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
        response = self.extractor_get_csv()
        with open(self._output_path, 'wt') as f:
            f.write(response.text)

    def execute(self):
        super(CsvDownload, self).execute()
        self.download_csv()


def main():
    cli = CsvDownload()
    cli.execute()


if __name__ == '__main__':
    main()
