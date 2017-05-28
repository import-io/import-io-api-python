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

import argparse
import os


# - Inputs
#   * API Key
#   * Extractor Id
#   * Output directory
#   * file naming format
# - Outputs
#   * File in file system


class AdBase(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser(description=self.cli_description())
        self._args = None
        self._api_key = os.environ['IMPORT_IO_API_KEY']
        self._extractor_id = None
        self._crawl_run_id = None
        self._output_directory = None
        self._input_path = None
        self._output_path = None

    def add_api_key_arg(self, required=True):
        """
        Adds command line argument to handle passing the API Key on the command line
        :return: None
        """
        self._parser.add_argument('-a', '--api-key', action='store', dest='api_key', required=required,
                                  metavar='api_key', help='Import.io API key from user account')

    def add_extractor_id_arg(self, required=True):
        """
        Adds a command line argument to handle processing of extractor Id
        :return: None
        """
        self._parser.add_argument('-e', '-extractor-id', action='store', dest='extractor_id', metavar='extractor_id',
                                  required=required, help='Identifies the extractor to be accessed')

    def add_crawl_run_id_arg(self, required=True):
        """
        Adds a command line argument to handle processing of crawl run Id
        :return: None
        """
        self._parser.add_argument('-r', '-crawl-run-id', action='store', dest='extractor_id', metavar='extractor_id',
                                  required=required, help='Identifies the crawl run to be accessed')

    def add_output_directory_arg(self, required=False):
        """
        Adds a command line argument to handle processing of output directory
        :return: None
        """
        self._parser.add_argument('-d', '--output-dir', action='store', dest='output_directory', metavar='path',
                                  required=required, default=os.path.curdir,
                                  help='Path to output directory, default is current directory')

    def add_file_input_path_arg(self, required=True):
        self._parser.add_argument('-i', '--input-file', action='store', dest='input_path', metavar='path',
                                  required=required, help="Path to input file")

    def add_file_output_path_arg(self, required=True):
        self._parser.add_argument('-o', '--output-file', action='store', dest='output_path', metavar='path',
                                  required=required, help="Path to output file")

    def cli_description(self):
        """
        Description of the CLI command, child classes are required to override
        :return: None
        """
        return None

    def handle_arguments(self):
        """
        Implements argument handling by argparse. Child classes are required to
        calls this after they add their own arguments
        :return:
        """
        self._args = self._parser.parse_args()

    def get_arguments(self):
        """
        Fetches command line arguments after they have been parsed. Child classes are
        required to call this method and then perform any fetches specific to their class
        :return: None
        """
        if 'api_key' in self._args:
            self._api_key = self._args.api_key

        if 'extractor_id' in self._args:
            self._extractor_id = self._args.extractor_id

        if 'crawl_run_id' in self._args:
            self._crawl_run_id = self._args.crawl_run_id

        if 'output_directory' in self._args:
            self._output_directory = self._args.output_directory

        if 'input_path' in self._args:
            self._input_path = self._args.input_path

        if 'output_path' in self._args:
            self._output_path = self._args.output_path

    def execute(self):
        self.handle_arguments()


class AdDatabase(AdBase):
    def __init__(self):
        super(AdDatabase, self).__init__()
        self._db_user = None
        self._db_password = None
        self._db_database = None
        self._db_host = None

    def add_database_arguments(self):
        self._parser.add_argument('-u', '--user', action='store', dest='db_user', required=True, metavar='user',
                                  help='User name to use for authentication to the database')
        self._parser.add_argument('-p', '--password', action='store', dest='db_password', required=True,
                                  metavar='password',
                                  help='Password to use for authentication to the database')
        self._parser.add_argument('-d', '--database', action='store', dest='db_database', required=True,
                                  metavar='database',
                                  help='Database to use')
        self._parser.add_argument('-i', '--host', action='store', dest='db_host', required=True, metavar='hostname',
                                  help='Hostname or IP address of the database')

    def handle_arguments(self):
        self.add_database_arguments()

        super(AdDatabase, self).handle_arguments()

    def get_arguments(self):
        super(AdDatabase, self).get_arguments()

        if 'db_user' in self._args:
            self._db_user = self._args.db_user

        if 'db_password' in self._args:
            self._db_password = self._args.db_password

        if 'db_database' in self._args:
            self._db_database = self._args.db_database

        if 'db_host' in self._args:
            self._db_host = self._args.db_host


