from typing import Dict, List
from os import listdir, environ
from os.path import join

import requests
from markdown import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension
from atlassian import Confluence

workspace = environ.get('GITHUB_WORKSPACE')
if not workspace:
    raise Exception('No workspace is set')


envs: Dict[str, str] = {}
for key in ['from', 'parent_id', 'cloud', 'user', 'token']:
    value = environ.get(f'INPUT_{key.upper()}')
    if not value:
        raise Exception(f'Missing value for {key}')
    envs[key] = value


try:
    confluence = Confluence(
        url='https://picklerobot.atlassian.net',
        username="simrun@picklerobot.com",
        password=envs['token'],
        cloud=True)
except:
    print("Connection did not work")
with open(join(workspace, envs['from'])) as f:
    md = f.read()

# url = f"https://{envs['cloud']}.atlassian.net/wiki/rest/api/content/{envs['to']}"

# current = requests.get(url, auth=(envs['user'], envs['token'])).json()

html = markdown(md, extensions=[GithubFlavoredMarkdownExtension()])
# content = {
#     'id': current['id'],
#     'type': current['type'],
#     'title': current['title'],
#     'version': {'number': current['version']['number'] + 1},
#     'body': {
#         'editor': {
#             'value': html,
#             'representation': 'editor'
#         }
#     }
# }
confluence.create_page(space= "Engineering", title="Release Notes", body=html, parent_id=envs['parent_id'])

# updated = requests.put(url, json=content, auth=(
#     envs['user'], envs['token'])).json()
# link = updated['_links']['base'] + updated['_links']['webui']
# print(f'Uploaded content successfully to page {link}')
