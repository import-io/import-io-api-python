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
from importio2 import ExtractorAPI
from pprint import pprint


# Given the contents in the file urls.txt

extractor_id = '7d9122f6-f293-49e4-8035-1961dac6f049'

url_list = list()
url_list.append("http://www1.example.com")
url_list.append("http://www2.example.com")
url_list.append("http://www3.example.com")
url_list.append("http://www4.example.com")
url_list.append("http://www5.example.com")
url_list.append("http://www6.example.com")
url_list.append("http://www7.example.com")
url_list.append("http://www8.example.com")
url_list.append("http://www9.example.com")

api = ExtractorAPI()

# Upload a list of URLs to an extractor
api.put_url_list(extractor_id, url_list)


# Download a list of URLs to an extractor

url_list = api.get_url_list(extractor_id)
pprint(url_list)
