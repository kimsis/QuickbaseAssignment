import requests
from time import time
import time
from pprint import pprint
from externals import username, freshdeskUrl, githubUrl, token_freshdesk, token_github

def get_user():
    response = requests.get(f'{githubUrl}/users/{username}', auth=(username, token_github)).json()
    return response

def get_contact(id):
    headers = {
        'Content-Type': 'application/json',
    }
    try:
        response = requests.get(f'{freshdeskUrl}/contacts/{id}', headers=headers, auth=(token_freshdesk, 'X'))
        json = response.json()
        return json
    except:
        return response.status_code

def get_false_contact(id):
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.get(f'{freshdeskUrl}/contacts/{id}', headers=headers, auth=(token_freshdesk, 'X'))
    return response

def post_contact(user):
    # Adding current datetime to make the email unique,
    # as the freshdesk API needs 30 minutes to delete a contact
    email = str(time.time()) + user['email']
    json_data = {
        'name': user['name'],
        'email': email,
        'address': user['location'],
        'description': user['bio'],
    }

    response = requests.post(f'{freshdeskUrl}/contacts', json=json_data, auth=(token_freshdesk, 'X')).json()
    return response

def delete_contact(id):
    status_code = requests.delete(f'{freshdeskUrl}/contacts/{id}/hard_delete?force=true', auth=(token_freshdesk, 'X')).status_code
    return status_code

if(__name__ == '__main__'):
    user = get_user()
    id = post_contact(user)['id']
    contact = get_contact(id)
    delete_contact(id)