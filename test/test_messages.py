from test.test_common import TestCommon


class TestBaseMessages(TestCommon):

    def setUp(self) -> None:
        super(TestBaseMessages, self).setUp()
        self.path = None

    def _create_room(self, members: list) -> str:
        for member in members:
            self.test_client.put('/users', json={'username': member})
        response = self.test_client.put('/rooms', json={'members': members})
        return response.json['room_id']

    def test_messages_amount__no_message(self):
        if not self.path:
            return

        # FIXTURE
        username = 'test_user'
        room_id = self._create_room([username, 'test_user2'])

        # EXECUTE
        response = self.test_client.get(
            f'/{self.path}/amount'
        )

        # VERIFY
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.json['amount'])

    def test_create_message__success_get_message(self):
        if not self.path:
            return

        # FIXTURE
        username = 'test_user'
        date = '2021-09-10T10:20:30.123000'
        message = 'This is a test'
        room_id = self._create_room([username, 'test_user2'])

        # EXECUTE
        response = self.test_client.put(
            f'/rooms/{room_id}/{self.path}',
            json={'username': username, 'date': date, 'message': message}
        )

        # VERIFY
        self.assertEqual(200, response.status_code)
        get_response = self.test_client.get(
            f'/rooms/{room_id}/{self.path}',
            json={'username': username}
        )
        messages = get_response.json
        self.assertEqual(1, len(messages))
        self.assertEqual({'from': username, 'date': date, 'message': message}, messages[0])
        get_amount_response = self.test_client.get(
            f'/{self.path}/amount'
        )
        self.assertEqual(1, get_amount_response.json['amount'])

    def test_get_messages__multiple_messages(self):
        if not self.path:
            return

        # FIXTURE
        expected_messages = [
            ('test_user', '2021-09-01T10:30:31', 'Test 1'),
            ('test_user2', '2021-09-01T10:30:32', 'Test 2'),
            ('test_user', '2021-09-10T10:30:31', 'Test 3'),
            ('test_user2', '2021-10-01T10:30:31', 'Test 4'),
        ]
        room_id = self._create_room(['test_user', 'test_user2'])
        for from_, date, message in expected_messages:
            response = self.test_client.put(
                f'/rooms/{room_id}/{self.path}',
                json={'username': from_, 'date': date, 'message': message}
            )
            self.assertEqual(200, response.status_code)

        # EXECUTE
        get_response = self.test_client.get(
            f'/rooms/{room_id}/{self.path}',
            json={'username': 'test_user2'}
        )

        # VERIFY
        self.assertEqual(200, get_response.status_code)
        messages = get_response.json
        self.assertEqual(4, len(messages))
        for i, message in enumerate(expected_messages):
            self.assertEqual({'from': message[0], 'date': message[1], 'message': message[2]}, messages[i])

    def test_get_messages__unordered_messages__return_ordered(self):
        if not self.path:
            return

        # FIXTURE
        expected_messages = [
            ('test_user', '2021-09-01T10:30:31', 'Test 1'),
            ('test_user2', '2021-09-01T10:30:32', 'Test 2'),
            ('test_user', '2021-09-10T10:30:31', 'Test 3'),
            ('test_user2', '2021-10-01T10:30:31', 'Test 4'),
        ]
        room_id = self._create_room(['test_user', 'test_user2'])
        for from_, date, message in reversed(expected_messages):
            response = self.test_client.put(
                f'/rooms/{room_id}/{self.path}',
                json={'username': from_, 'date': date, 'message': message}
            )
            self.assertEqual(200, response.status_code)

        # EXECUTE
        get_response = self.test_client.get(
            f'/rooms/{room_id}/{self.path}',
            json={'username': 'test_user2'}
        )

        # VERIFY
        self.assertEqual(200, get_response.status_code)
        messages = get_response.json
        self.assertEqual(4, len(messages))
        for i, message in enumerate(expected_messages):
            self.assertEqual({'from': message[0], 'date': message[1], 'message': message[2]}, messages[i])

    def test_get_messages__with_last_seen__return_from_last_seen(self):
        if not self.path:
            return

        # FIXTURE
        expected_messages = [
            ('test_user', '2021-09-01T10:30:31', 'Test 1'),
            ('test_user2', '2021-09-01T10:30:32', 'Test 2'),
            ('test_user', '2021-09-10T10:30:31', 'Test 3'),
            ('test_user2', '2021-10-01T10:30:31', 'Test 4'),
        ]
        room_id = self._create_room(['test_user', 'test_user2'])
        for from_, date, message in reversed(expected_messages):
            response = self.test_client.put(
                f'/rooms/{room_id}/{self.path}',
                json={'username': from_, 'date': date, 'message': message}
            )
            self.assertEqual(200, response.status_code)

        # EXECUTE
        get_response = self.test_client.get(
            f'/rooms/{room_id}/{self.path}',
            json={'username': 'test_user2', 'last_seen': '2021-09-01T10:30:32'}
        )

        # VERIFY
        self.assertEqual(200, get_response.status_code)
        messages = get_response.json
        self.assertEqual(2, len(messages))
        for i, message in enumerate(expected_messages[2:]):
            self.assertEqual({'from': message[0], 'date': message[1], 'message': message[2]}, messages[i])
     
            
class TestMessages(TestBaseMessages):

    def setUp(self) -> None:
        super(TestMessages, self).setUp()
        self.path = 'messages'


class TestSimpleMessages(TestBaseMessages):

    def setUp(self) -> None:
        super(TestSimpleMessages, self).setUp()
        self.path = 'simple_messages'
