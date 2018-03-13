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
import logging
import sys
import os
from importio2 import ExtractorAPI
from importio2 import CrawlRunAPI
from jinja2 import Template, FileSystemLoader, Environment

logger = logging.getLogger(__name__)


class CrawlRunMetadata(object):

    def __init__(self):
        pass


class ExtractorMetadata(object):

    def __init__(self,
                 guid, parent_guid, chained, name, fields, create_timestamp, modified_timestamp):
        self.create_timestamp = create_timestamp
        self.modified_timestamp = modified_timestamp
        self.crawl_runs = []
        self.fields = fields
        self.name = name
        self.guid = guid
        self.parent_guid = parent_guid
        self.chained = chained


class ExtractorDocumentGenerator(object):

    def __init__(self):
        self._filter = None
        self._template = None

    def handle_arguments(self):
        parser = argparse.ArgumentParser(description="Generates Extractor Documentation")
        parser.add_argument('-c', '--configuration', action='store', dest='configuration', metavar='path',
                            required=True, help="Configuration data for documentation generation")
        parser.add_argument('-f', '--filter', action='store', dest='filter', metavar='regexp',
                            help="Filter Extractors based on Regular Expression")
        parser.add_argument('-t', '--template', action='store', dest='template', metavar='path',
                            required=True, help="Path to jina2 template for generating output")
        args = parser.parse_args()

        if args.filter is not None:
            self._filter = args.filter

        if args.template is not None:
            self._template = args.template

    def get_extractor_ids(self):
        """
        Extractors the required metadata from
        :return:
        """
        api = ExtractorAPI()
        extractors = api.list()
        extractor_list = []

        for extractor in extractors:
            f = extractor['fields']
            chained = False
            parent_guid = None
            if 'isChained' in f:
                chained = bool(f['isChained'])
            if 'parentExtractorGuid' in f:
                parent_guid = f['parentExtractorGuid']

            e = ExtractorMetadata(guid=f['guid'],
                                  parent_guid=parent_guid,
                                  name=f['name'],
                                  fields=f['fields'],
                                  create_timestamp=f['_meta']['creationTimestamp'],
                                  modified_timestamp=f['_meta']['timestamp'],
                                  chained=chained
                                  )
#            print(extractor)
            extractor_list.append(e)
        return extractor_list

    def generate(self, extractors):
        template_loader = FileSystemLoader(searchpath='./')
        template_env = Environment(loader=template_loader)

        t = template_env.get_template(self._template)
        template_vars = {
            "title": "Extractor Documentation",
            "extractors": extractors,
        }
        print(t.render(template_vars))

    def generate_documentation(self):
        extractors = self.get_extractor_ids()
        leaf_extractors = []
        for e in extractors:
            if e.parent_guid is not None:
                leaf_extractors.append(e)

        self.generate(leaf_extractors)

    def execute(self):
        self.handle_arguments()
        self.generate_documentation()


def main():
    cli = ExtractorDocumentGenerator()
    cli.execute()


if __name__ == '__main__':
    main()
