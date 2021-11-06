
from test.test_common import TestCommon


class TestUsers(TestCommon):

    def test_get_users__no_user__return_empty(self):
        # EXECUTE
        response = self.test_client.get('/users')

        # VERIFY
        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json)

    def test_create_user__create_user_and_get_it(self):
        # EXECUTE
        create_response = self.test_client.put('/users', json={'username': 'myuser', 'name': 'My Test'})
        get_response = self.test_client.get(f'/users/myuser')

        # VERIFY
        self.assertEqual(200, create_response.status_code)
        self.assertEqual(200, get_response.status_code)
        self.assertEqual({'name': 'My Test', 'username': 'myuser'}, get_response.json)

    def test_create_multiple_users__get_all_created_users(self):
        # FIXTURE
        users = ('test1', 'test2', 'test3', 'test4')
        for user in users:
            create_response = self.test_client.put('/users', json={'username': user, 'name': user})
            self.assertEqual(200, create_response.status_code)

        # EXECUTE
        get_response = self.test_client.get(f'/users')

        # VERIFY
        self.assertEqual(set(users), {u['username'] for u in get_response.json})
