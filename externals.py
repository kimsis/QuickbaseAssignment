import os
import sys

# Set username and tokens from the environment variables
#print('Please enter username:')
#username = input()
username = sys.argv[1]
print(f'Username: {username}')

#print('Please enter freshdesk subdomain:')
#freshdesk_subdomain = input()
freshdesk_subdomain = sys.argv[2]
print(f'Subdomain: {freshdesk_subdomain}')

freshdeskUrl = f'https://{freshdesk_subdomain}.freshdesk.com/api/v2'
githubUrl = f'https://api.github.com'

token_github = os.getenv('GITHUB_TOKEN')
token_freshdesk = os.environ.get('FRESHDESK_TOKEN')
