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
import csv
import logging
import os
from configparser import ConfigParser

from dateutil import parser as date_parser

from importio2.commands import AdBase
from importio2.commands import ChangeOwnership
from importio2.commands import CreateCrawlRun
from importio2.commands import CsvToCrawlRun
from importio2.commands import CsvToJson
from importio2.commands import Date2Epoch
from importio2.commands import JsonToCrawlRun
from importio2.version import __version__ as api_version

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)


class UploadData(AdBase):
    def __init__(self):
        super(UploadData, self).__init__()
        self._target_extractor_id = None
        self._config_path = None
        self._csv_file_name_pattern = None
        self._json_file_name_pattern = None
        self._csv_data_file_path = None
        self._json_data_file_path = None
        self._data_directory = None
        self._date = None
        self._csv_directory = None
        self._json_directory = None
        self._crawl_run_id = None
        self._year = None
        self._month = None
        self._day = None

    def cli_description(self):
        """
        Returns a description of this command
        :return:
        """
        return 'Handles uploading data to an Extractor Crawl Run'

    def handle_arguments(self):
        """
        Adds the arguments for this specific command
        :return:
        """
        self._parser.add_argument('-c', '--config-path', action='store', dest='config_path',
                                  metavar='YYYY-MM-DD', required=True, help='Path to configuration file')
        self._parser.add_argument('-l', '--log-level', action='store', dest='log_level', default='notset',
                                  choices=['debug', 'info', 'warning', 'error', 'critical'], required=False,
                                  help='Sets the logging level')
        self._parser.add_argument('-d', '--date', action='store', dest='date',
                                  metavar='YYYY-MM-DD', required=True, help='Date of data in file')
        self._parser.add_argument('--version', action='version', version="api: {0}".format(api_version))

        super(UploadData, self).handle_arguments()

    def get_arguments(self):
        """
        Retrieves the specific arguments required by this command
        :return:
        """
        super(UploadData, self).get_arguments()

        if self._args.config_path is not None:
            self._config_path = self._args.config_path
        if self._args is not None:
            self._date = date_parser.parse(self._args.date)
        if self._args.log_level is not None:
            logging.basicConfig(level=logging.getLevelName(self._args.log_level.upper()))

    def load_configuration(self):
        """
        Loads the static configuration information from a file
        :return: None
        """
        configuration = ConfigParser()
        configuration.read(filenames=self._config_path)
        self._target_extractor_id = configuration.get('extractors', 'target_extractor_id')
        self._csv_file_name_pattern = configuration.get('paths', 'csv_file_name_pattern')
        self._json_file_name_pattern = configuration.get('paths', 'json_file_name_pattern')
        self._data_directory = configuration.get('paths', 'data_directory')
        self._csv_directory = configuration.get('paths', 'csv_directory')
        self._json_directory = configuration.get('paths', 'json_directory')
        logger.debug('target_extractor_id: {0}'.format(self._target_extractor_id))
        logger.debug('cvs_file_name_pattern: {0}'.format(self._csv_file_name_pattern))
        logger.debug('json_file_name_pattern: {0}'.format(self._json_file_name_pattern))
        logger.debug('data_directory: {0}'.format(self._data_directory))
        logger.debug('csv_directory: {0}'.format(self._csv_directory))
        logger.debug('json_directory: {0}'.format(self._json_directory))

    def get_input_file_paths(self):
        """
        Generates the complete path to CSV file to load
        :return: None
        """
        self._csv_data_file_path = os.path.join(os.path.abspath(self._data_directory),
                                                self._date.strftime(self._csv_file_name_pattern))
        self._json_data_file_path = os.path.join(os.path.abspath(self._data_directory),
                                                 self._date.strftime(self._json_file_name_pattern))
        logger.info("CSV data file path: {0}, JSON data file path: {1}".format(self._csv_data_file_path,
                                                                               self._json_data_file_path))

    def initialize(self):
        """
        Initialization steps before processing data
        :return:
        """
        self.load_configuration()

    def convert_csv_to_json(self):
        """
        Converts the data in CSV format to JSON
        :return:
        """
        converter = CsvToJson()
        converter.run(self._csv_data_file_path, self._json_data_file_path)

    @staticmethod
    def get_row_count(file_path):
        count = 0
        with open(file_path) as f:
            # Remove the header
            f.readline(1)
            reader = csv.DictReader(f)
            for row in reader:
                count += 1
        return count

    def create_crawl_run(self):
        """
        Creates a crawl run in the target extractor
        :return:
        """
        d2e = Date2Epoch()
        start, stop = d2e.run(self._date.year, self._date.month, self._date.day)
        row_count = ProcessData.get_row_count(self._csv_data_file_path)
        crawl_run_factory = CreateCrawlRun()
        crawl_run_factory.run(self._target_extractor_id,
                              failed_url_count=0,
                              success_url_count=row_count,
                              row_count=row_count,
                              total_url_count=row_count,
                              started_at=start,
                              stopped_at=stop,
                              state='FINISHED')

    def add_csv_to_crawl_run(self):
        """
        Adds the CSV data file to a crawlrun
        :return:
        """
        csv_to_crawl_run = CsvToCrawlRun()
        csv_to_crawl_run.run(self._crawl_run_id, csv_path=self._csv_data_file_path)

    def add_json_to_crawl_run(self):
        """
        Adds the JSON data file to a crawlrun
        :return:
        """
        json_to_crawl_run = JsonToCrawlRun()
        json_to_crawl_run.run(self._crawl_run_id, json_path=self._json_data_file_path)

    def change_owner_of_crawl_run(self):
        changer = ChangeOwnership()
        changer.run(object_id=self._crawl_run_id, object_type='crawlrun')

    def process_data(self):
        """
        Handle the processing of a single file/date combination
        :return:
        """
        # Step 1 - Convert CSV file to JSON document
        # self.convert_csv_to_json()

        # Step 2 - Create crawl run with the specified file date
        # self.create_crawl_run()

        # Step 3 - Add CSV file to crawl run
        # self.add_csv_to_crawl_run()

        # Step 4 - Add JSON file to crawl run
        # self.add_json_to_crawl_run()

        # Step 5 - Change Owner of Crawl-run
        # self.change_owner_of_crawl_run()

    def run(self, config_path, date):
        self._config_path = config_path
        self._date = date

    def execute(self):
        self.handle_arguments()
        self.initialize()
        self.process_data()


def main():
    cli = UploadData()
    cli.execute()


if __name__ == '__main__':
    main()
