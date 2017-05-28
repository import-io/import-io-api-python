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
import csv
import logging
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

DEFAULT_RESOURCE_ID = 'F' * 32


class CsvToJson(AdBase):

    def __init__(self):
        super(CsvToJson, self).__init__()
        logging.basicConfig(level=logging.ERROR)
        self._csv_path = None
        self._json_path = None
        self._overwrite = False
        self._date = None
        self._remove_bom = False

    def handle_arguments(self):
        self._parser.add_argument('--csv-path', action='store', dest='csv_path', metavar='path', required=True,
                                  help='Path to CSV file to transform')
        self._parser.add_argument('--json-path', action='store', dest='json_path', metavar='path', required=True,
                                  help='Destination path of JSON document')
        self._parser.add_argument('--overwrite', action='store_true', dest='overwrite',
                                  help='Flag to explicitly set to overwrite file if it exists')
        self._parser.add_argument('--remove-bom', action='store_true', dest='remove_bom', default=False,
                                  help='Remove byte mark order')

        super(CsvToJson, self).handle_arguments()

        self.get_arguments()

    def get_arguments(self):
        super(CsvToJson, self).get_arguments()

        if 'csv_path' in self._args:
            self._csv_path = self._args.csv_path
        if 'json_path' in self._args:
            self._json_path = self._args.json_path
        if 'overwrite' in self._args:
            self._overwrite = self._args.overwrite
        if 'date' in self._args:
            self._date = self._args.date
        if 'remove_bom':
            self._remove_bom = self._args.remove_bom

    def base_document(self, url, resource_id, timestamp, sequence_number, status_code=200):
        """
        Generates the base document for each URL
        :param url: Source of the URL with the result
        :param resource_id: Import.io resource Id
        :param timestamp: Timestamp of when the data was fetched in Unix epoch in milliseconds
        :param sequence_number: Row number
        :param status_code: HTTP status code from fetching results from URL
        :return:
        """
        document = {}
        document['url'] = url
        document['result'] = {}
        document['result']['timestamp'] = timestamp
        document['result']['sequenceNumber'] = sequence_number
        document['result']['pageData'] = {
            'resourceId': resource_id, 'statusCode': status_code, 'timestamp': timestamp}
        document['result']['extractorData'] = {}
        document['result']['extractorData']['url'] = url
        document['result']['extractorData']['resourceId'] = resource_id
        document['result']['extractorData']['data'] = []
        document['result']['extractorData']['data'].append({})
        document['result']['extractorData']['data'][0]['group'] = []
        return document

    def row_to_group_instance(self, row, columns):
        """
        Generates a row of data contains within a group
        :param row: A single row of data from the CSV file
        :param columns: The columns from the header of the CSV file
        :return: A dictionary of the transformed row
        """
        d = {}
        for col in columns:
            d[col] = []
            d[col].append({'text': row[col]})
        return d

    def write_document(self, document_list):
        with open(self._json_path, 'w') as json_file:
            first = True
            for document in document_list:
                if first:
                    first = False
                else:
                    json_file.write('\n')
                # Append to file in compact form with no spaces
                json.dump(document, json_file, separators=(',', ':'))

    def csv_to_json(self):
        with open(self._csv_path) as csv_file:
            if self._remove_bom:
                dummy = csv_file.read(1)
            csv_reader = csv.DictReader(csv_file)

            # Get the field names from the CSV and
            # remove the first column which contains the URL
            fields = csv_reader.fieldnames
            headers = fields[1:]
            logger.debug("CSV headers: {0}".format(headers))

            last_url = None
            group = None
            document = None
            document_list = []
            sequence_number = 0
            for row in csv_reader:
                url = row['url']
                if last_url != url:
                    ts = int(datetime.now().strftime('%s')) * 1000
                    document = self.base_document(url=url, resource_id=DEFAULT_RESOURCE_ID,
                                                  timestamp=ts, sequence_number=sequence_number)
                    group = document['result']['extractorData']['data'][0]['group']
                    document_list.append(document)
                    sequence_number += 1
                group.append(self.row_to_group_instance(row, headers))
                last_url = url
        # If file exists then throw and exception unless the
        # override flag is set
        if not self._overwrite and os.path.exists(self._json_path):
            msg = "File: {0} exists. Use --overwrite flag to allow".format(self._json_path)
            raise Exception(msg)

        with open(self._json_path, 'w') as json_file:
            first = True
            for document in document_list:
                if first:
                    first = False
                else:
                    json_file.write('\n')
                # Append to file in compact form with no spaces
                json.dump(document, json_file, separators=(',', ':'))

    def run(self, csv_path, json_path, overwrite=True):
        self._csv_path = csv_path
        self._json_path = json_path
        self._overwrite = overwrite
        self.csv_to_json()

    def execute(self):
        try:
            self.handle_arguments()
            self.csv_to_json()
        except Exception as e:
            logger.exception(e)


def main():
    cli = CsvToJson()
    cli.execute()

if __name__ == '__main__':
    main()
