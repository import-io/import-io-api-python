import sys
import requests
from pprint import pprint
import argparse

parser = argparse.ArgumentParser(description="Duplicates an Extractor from an account to another account")
parser.add_argument('--source-api-key', action='store', dest='source_api_key', metavar='guid', required=True,
                    help='Source account API Key')
parser.add_argument('--target-api-key', action='store', dest='target_api_key', metavar='guid', required=True,
                    help='Target account API Key')
parser.add_argument('--extractor-id', action='store', dest='extractor_id', metavar='guid', required=True,
                    help='Extractor Id')
args = parser.parse_args()

source = 'store.import.io'
# source_api_key = 'f59043c4763b4067/e8d65bd216da373777aa8ce61fda03406d06f829122f719ef6697c804c82742374000699b716b66c6501e1bb1a235968c3639c0a25ca2ab125537e28c32084ffccd6601d4d5bd5173'
source_api_key = args.source_api_key
target = 'store.demo-owl.com'
# target_api_key = 'd9eb13ee69b34f8cae4bc14e857f680957ce95d5c23ecf4d9c8fb8fbe1f181f1956fa88bf99a058c941025f1db71ace948740e4d53483963a27f3e84e4c05aaf4158d5e5b7c6e5e01cc94bce277b2543'
target_api_key = args.target_api_key

extractor_guid = args.extractor_id

def get_owner():
    return requests.get('http://api.%s/auth/currentuser?_apikey=%s' % (target.replace('store.', ''), target_api_key)).json()


target_owner = get_owner()

copied = {}


def copy(object_name, guid):
    schema = requests.get('https://%s/store/%s/_schema?_apikey=%s' % (source, object_name, source_api_key)).json()

    print('copy https://{0}/store/{1}/{2}'.format(source, object_name, guid))
    old_obj = requests.get('https://%s/store/%s/%s?_apikey=%s' % (source, object_name, guid, source_api_key)).json()
    attachments = []
    sub_objects = []
    for key in old_obj.keys():
        if key not in schema['properties']:
            del old_obj[key]
        elif schema['properties'][key].get('readOnly', False):
            del old_obj[key]
        elif schema['properties'][key].get('referenceBucket', None):
            if old_obj[key] in copied:
                old_obj[key] = copied[old_obj[key]]
            else:
                sub_objects.append({
                    'key': key,
                    'object_name': schema['properties'][key]['referenceBucket'],
                    'guid': old_obj[key],
                })
                del old_obj[key]
        elif schema['properties'][key].get('attachment', False):
            attachments.append({
                'key': key,
                'guid': old_obj[key],
            })
            del old_obj[key]
    
    new_obj = requests.post('https://%s/store/%s?_apikey=%s' % (target, object_name, target_api_key), json=old_obj).json()
    requests.patch('https://%s/store/%s/%s?newOwner=%s&_apikey=%s' % (target, object_name, new_obj['guid'], target_owner, target_api_key))
    copied[guid] = new_obj['guid']

    for attachment in attachments:
        print('copy attachment https://{0}/store/{1}/{2}/_attachment/{3}/{4}'.format(source, object_name, guid, attachment['key'], attachment['guid']))
        r = requests.get('https://%s/store/%s/%s/_attachment/%s/%s?_apikey=%s'% (
            source, object_name, guid, attachment['key'], attachment['guid'], source_api_key))
        requests.put('https://%s/store/%s/%s/_attachment/%s?_apikey=%s' % (
            target, object_name, new_obj['guid'], attachment['key'], target_api_key),
            headers={'content-type': r.headers['content-type']}, data=r.content)

    for sub_object in sub_objects:
        print('copy sub_object {0}'.format(sub_object['key']))
        obj = copy(sub_object['object_name'], sub_object['guid'])
        new_obj[sub_object['key']] = obj['guid']
        requests.patch('https://%s/store/%s/%s?_apikey=%s' % (target, object_name, new_obj['guid'], target_api_key),
                       json={sub_object['key']: obj['guid']})

    return new_obj


def copy_extractor(extractor_guid):
    return copy('extractor', extractor_guid)


def list_crawlruns(extractorId):
    json = requests.get('https://%s/store/crawlrun/_search?_sort=_meta.creationTimestamp&_page=1&_perpage=30&extractorId=%s&_apikey=%s' % (source, extractorId, source_api_key)).json()
    return [x['fields'] for x in json['hits']['hits']]


def copy_crawlrun(guid):
    crawlrun = copy('crawlrun', guid)


def copy_extractor_and_crawlruns(guid):
    extractor = copy_extractor(guid)
    for crawlrun in list_crawlruns(guid):
        copy_crawlrun(crawlrun['guid'])
    return extractor


if __name__ == '__main__':
    pprint(copy_extractor_and_crawlruns(extractor_guid))
