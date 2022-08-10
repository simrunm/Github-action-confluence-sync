from typing import Dict
from os import environ
from os.path import join
from markdown import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension
from atlassian import Confluence
from bs4 import BeautifulSoup

# Get info from Github action
workspace = environ.get('GITHUB_WORKSPACE')
if not workspace:
    raise Exception('No workspace is set')
    
envs: Dict[str, str] = {}
for key in ['from', 'parent_id', 'user', 'token']:
    value = environ.get(f'INPUT_{key.upper()}')
    if not value:
        raise Exception(f'Missing value for {key}')
    envs[key] = value

# Connect to confluence
confluence = Confluence(
    url='https://picklerobot.atlassian.net',
    username=envs['user'], 
    password=envs['token'],
    cloud=True)

# Read Markdown file
with open(join(workspace, envs['from'])) as f:
    md = f.read()

# Convert to html and split title and body
html = markdown(md, extensions=[GithubFlavoredMarkdownExtension()])
Soup = BeautifulSoup(html, features="html.parser")
title = f'Release Notes {Soup.find_all("h2")[0].text.strip()}'
body = "\n".join(html.split('\n')[1:])

# Get space id and create page
space_key = confluence.get_page_space(envs['parent_id'])
confluence.create_page(space=space_key, title=title, body=body, parent_id=envs['parent_id'])
