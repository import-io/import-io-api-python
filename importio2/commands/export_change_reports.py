#
# Copyright 2017-2018 Import.io
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
import logging
from importio2.commands import AdBase
from importio2 import ReportAPI

logger = logging.getLogger(__name__)


class ExportChangeReports(AdBase):

    def __init__(self):
        pass

    def get_description(self):
        parser = argparse.ArgumentParser(description="Export all of the change reports from an account")

    def handle_arguments(self):
        super(ExportChangeReports, self).handle_arguments()
        parser = argparse.ArgumentParser(description="Export all of the change reports from an account")
        pass

    def get_arguments(self):
        pass

    def get_reports(self):
        return []

    def get_report_runs(self, report):
        return []

    def get_report_run(self, report_run):

    def execute(self):
        pass


def main():
    cli = ExportChangeReports()
    cli.execute()


if __name__ == '__main__':
    main()
