#!/usr/bin/env python
#
# Copyright 2016 Import.io
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

extractor_id = '3ffe6b46-c6dd-4730-a8cf-098426dda22b'

inputs = list()
inputs.append('{"_url":"https://www.chilis.com/locations","zipcode":"95037"}')
inputs.append('{"_url":"https://www.chilis.com/locations","zipcode":"95118"}')
inputs.append('{"_url":"https://www.chilis.com/locations","zipcode":"95119"}')
inputs.append('{"_url":"https://www.chilis.com/locations","zipcode":"95120"}')
inputs.append('{"_url":"https://www.chilis.com/locations","zipcode":"95123"}')
inputs.append('{"_url":"https://www.chilis.com/locations","zipcode":"95141"}')

api = ExtractorAPI()

inputs_id = api.put_inputs(extractor_id, inputs)
pprint(inputs_id)

inputs = api.get_inputs(extractor_id)
pprint(inputs)
