#!/usr/bin/env python

import argparse
import fnmatch
import logging
import os

from dateutil import parser

from importio2.commands import AdBase, CsvToJson

logger = logging.getLogger(__name__)


class DataUpload(AdBase):
    """
    """

    def __init__(self):
        super(DataUpload, self).__init__()
        self.extractor_id = None
        self.timestamp = None
        self.upload_directory = None

    def cli_description(self):
        return 'Uploads data from base file'

    def handle_arguments(self):
        arg_parser = argparse.parser = argparse.ArgumentParser(description=self.cli_description())

        arg_parser.add_argument('-d', '--upload-directory', action='store', dest="upload_directory", required=False,
                                metavar='path', default=os.path.curdir,
                                help="Upload directory defaults to current directory")

        arg_parser.add_argument('-e', '--extractor-id', action='store', dest='extractor_id', required=True,
                                metavar='id',
                                help='Extractor to upload date to')

        arg_parser.add_argument('-t', '--timestamp', action='store', dest='timestamp', required=True, metavar='date',
                                help='Date of upload')

        args = arg_parser.parse_args()

        if 'upload_directory' in args:
            self._upload_directory = args.upload_directory

        if 'extractor_id' in args:
            self._extractor_id = args.extractor_id

        if 'timestamp' in args:
            self._timestamp = parser.parse(args.timestamp)

    def find(self, pattern, path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result

    def get_csv_path(self):
        pattern = "*{0}-{1}-{2}.csv".format(self._timestamp.year, self._timestamp.month, self._timestamp.day)
        csv_directory = os.path.join(self._upload_directory, 'csv')
        csv_path = self.find(pattern, csv_directory)
        return csv_path

    def get_json_path(self):
        json_path = None
        return json_path

    def csv_to_json(self):
        """
        Translates a CSV to JSON file
        :return: 
        """
        csv_to_json = CsvToJson()

        csv_path = self.get_csv_path()
        json_path = self.get_json_path()

        csv_to_json.run(csv_path, json_path)

    def create_crawl_run(self):
        pass

    def add_csv_to_crawl_run(self):
        pass

    def add_json_to_crawl_run(self):
        pass

    def change_owner_of_crawl_run(self):
        pass

    def upload(self):
        """
        Upload the CSV and JSON files to an extractor crawl run
        :return: 
        """

        # Step 1 : Copy CSV to JSON
        self.csv_to_json()

        # Step 2 : Create Crawl Run
        self.create_crawl_run()

        # Step 3 : Add the CSV file to the crawl run
        self.add_csv_to_crawl_run()

        # Step 4 : Add the JSON file the the crawl run
        self.add_json_to_crawl_run()

        # Step 5 : Change permission of crawl run
        self.change_owner_of_crawl_run()

    def run(self, extractor_id, timestamp, upload_directory=os.path.curdir):
        """
        Perform the operation of this instance
        
        :param extractor_id: Identifies the extractor to user
        :param timestamp: Day the data is for
        :param upload_directory: Upload load directory
        :return: 
        """
        self.upload_directory = upload_directory
        self.extractor_id = extractor_id
        self.timestamp = timestamp

    def execute(self):
        try:
            self.handle_arguments()
            self.upload()
        except Exception as e:
            logger.exception(e)


def main():
    cli = DataUpload()
    cli.execute()


if __name__ == '__name__':
    main()
