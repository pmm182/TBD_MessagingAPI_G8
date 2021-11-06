from test.test_common import TestCommon


class TestRooms(TestCommon):

    def test_create_room__user_does_not_exist__return_404(self):
        # EXECUTE
        response = self.test_client.put('/rooms', json={'members': ['test_user']})

        # VERIFY
        self.assertEqual(404, response.status_code)

    def test_create_room__no_member_passed__return_400(self):
        # EXECUTE
        response = self.test_client.put('/rooms', json={'members': []})

        # VERIFY
        self.assertEqual(400, response.status_code)

    def test_create_room__valid_members__room_created(self):
        # FIXTURE
        self.test_client.put('/users', json={'username': 'test_user'})
        self.test_client.put('/users', json={'username': 'test_user2'})

        # EXECUTE
        response = self.test_client.put('/rooms', json={'members': ['test_user', 'test_user2']})

        # VERIFY
        self.assertEqual(200, response.status_code)
        room_id = response.json['room_id']
        get_response = self.test_client.get('/rooms_by_user/test_user2')
        self.assertEqual(200, get_response.status_code)
        self.assertEqual(room_id, get_response.json[0]['id'])
        self.assertEqual({'test_user', 'test_user2'}, set(get_response.json[0]['members']))

    def test_get_rooms_by_user__multiple_rooms_with_same_user__return_all(self):
        # FIXTURE
        self.test_client.put('/users', json={'username': 'test_user'})
        self.test_client.put('/users', json={'username': 'test_user2'})
        self.test_client.put('/users', json={'username': 'test_user3'})
        response1 = self.test_client.put('/rooms', json={'members': ['test_user', 'test_user2']})
        response2 = self.test_client.put('/rooms', json={'members': ['test_user', 'test_user3']})
        response3 = self.test_client.put('/rooms', json={'members': ['test_user', 'test_user3', 'test_user2']})
        expected_room_ids = {response.json['room_id'] for response in (response1, response2, response3)}

        # EXECUTE
        get_response = self.test_client.get('/rooms_by_user/test_user')

        # VERIFY
        self.assertEqual(expected_room_ids, {room['id'] for room in get_response.json})

    def test_get_rooms_by_user__no_room_with_user__return_404(self):
        # FIXTURE
        self.test_client.put('/users', json={'username': 'test_user'})
        self.test_client.put('/users', json={'username': 'test_user2'})
        self.test_client.put('/rooms', json={'members': ['test_user', 'test_user2']})

        # EXECUTE
        get_response = self.test_client.get('/rooms_by_user/not_found')

        # VERIFY
        self.assertEqual(404, get_response.status_code)
