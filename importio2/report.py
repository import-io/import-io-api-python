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

from importio2.report_api_core import report_get


class ReportAPI (object):

    def __init__(self):
        pass

    def get(self, guid):
        """
        Fetches the report associated with the input guid
        :param guid: Unique identifier of the report
        :return: contents of the report as object
        """
        result = report_get()
        return

    def list(self):
        pass
