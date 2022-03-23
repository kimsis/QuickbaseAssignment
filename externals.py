import os
import inspect
from pprint import pprint
import sys

# Set username and tokens from the environment variables
username = sys.argv[1]
print(f'Username: {username}')

freshdesk_subdomain = sys.argv[2]
print(f'Subdomain: {freshdesk_subdomain}')

freshdeskUrl = f'https://{freshdesk_subdomain}.freshdesk.com/api/v2'
githubUrl = f'https://api.github.com'

token_github = os.getenv('GITHUB_TOKEN')
token_freshdesk = os.environ.get('FRESHDESK_TOKEN')