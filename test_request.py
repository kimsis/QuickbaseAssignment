import json
import unittest
import request
from unittest.mock import MagicMock, patch

mock_user = {'name': 'Dimitar', 'email': 'mimaqm@gmail.com', 'location': 'Eindhoven, North Brabant, Netherlands', 'bio': 'I am a junior level programmer, currently studying at Fontys Hogescholen. Here I store my personal projects, usually related to my studies.'}
# Slightly different dummy user, using the field names from freshdesk rather than github
mock_contact = {'name': 'Dimitar', 'address': 'Eindhoven, North Brabant, Netherlands', 'description': 'I am a junior level programmer, currently studying at Fontys Hogescholen. Here I store my personal projects, usually related to my studies.'}
# global id value, tried to use it for multiple tests on the same contact, however couldn't find a way to run the tests in a specific order, thus leaving it reduntant
id = 1

class TestRequest(unittest.TestCase):

    @patch('requests.get')
    def test_mock_get_user_success(self, mock_get_user):
        mock_get_user.return_value = MagicMock(status_code=200, json=lambda:mock_user)

        user_result = request.get_user()

        self.assertEqual(mock_user, user_result)

    @patch('requests.get')
    def test_mock_get_user_not_found(self, mock_get_user):
        # Make a mock result object and compare it with the processed one
        expected_result = json.loads('{"message": "Not Found", "documentation_url": "https://docs.github.com/rest/reference/users#get-a-user"}')
        mock_get_user.return_value = MagicMock(json=lambda:expected_result)

        mocked_result = request.get_user()

        self.assertEqual(expected_result, mocked_result)

    @patch('requests.post')
    def test_mock_post_contact_success(self, mock_post_contact):
        # Make a mock id and compare the resulting id with the expected
        mock_id = json.loads('{"id": 123456}')
        
        mock_post_contact.return_value = MagicMock(status_code=201, json=lambda:mock_id)
        user_result = request.post_contact(mock_user)

        self.assertEqual(123456, user_result['id'])

    def test_get_user_success(self):
        user_result = request.get_user()

        #self.assertDictContainsSubset(mock_user, user_result) deprecated
        self.assertLessEqual(mock_user.items(), user_result.items())

    def test_get_user_not_found(self):
        # Make a mock user, set it as return value and compare the end output from the get_user with the expected user object
        mock_result = json.loads('{"message": "Not Found", "documentation_url": "https://docs.github.com/rest/reference/users#get-a-user"}')
        
        # Setting a wrong username for the test, and changing it back afterwards
        request.username = 'kimsiz'
        user_result = request.get_user()
        request.username = 'kimsis'

        self.assertEqual(mock_result, user_result)

    def test_post_contact_invalid(self):
        # Save the user name, set it to none to test invalid post, and reset it back to its previous value
        expected_result = json.loads('{"description": "Validation failed", "errors": [{"field": "name", "message": "It should not be blank as this is a mandatory field", "code": "invalid_value"}]}')

        name = mock_user['name']
        mock_user['name'] = None
        user_result = request.post_contact(mock_user)
        mock_user['name'] = name

        self.assertEqual(expected_result, user_result)

    def test_get_contact_not_found(self):
        contact_result = request.get_contact(1)

        self.assertEqual(404, contact_result)

    def test_post_get_delete_contact_success(self):
        user_result = request.post_contact(mock_user)

        # Cannot test if mock_user is contained in user_result, as the user_result has different field names
        self.assertEqual(mock_user['name'], user_result['name'])
        self.assertEqual(mock_user['location'], user_result['address'])

        # Setting the id for the get and delete contact test
        global id
        id = user_result['id']

        contact_result = request.get_contact(id)

        # I kept the get and delete tests in the same function because I was unable to find a way to make these tests run after the post
        #self.assertDictContainsSubset(mock_user, user_result) deprecated
        self.assertLessEqual(mock_contact.items(), contact_result.items())

        result = request.delete_contact(id)

        self.assertEqual(204, result)
    
    def test_delete_invalid(self):
        result = request.delete_contact(1)

        self.assertEqual(404, result)

if(__name__ == '__main__'):
    unittest.main(argv=['first-arg-is-ignored'], exit=False)