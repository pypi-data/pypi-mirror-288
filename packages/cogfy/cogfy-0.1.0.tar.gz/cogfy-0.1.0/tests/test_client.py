import unittest
from unittest.mock import patch, MagicMock
from cogfy.client import CogfyClient

class TestCogfyClient(unittest.TestCase):
    def setUp(self):
        self.client = CogfyClient('http://example.com', 'fake_api_key')

    @patch('requests.get')
    def test_get_collections(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'test'}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = self.client.get_collections()
        self.assertEqual(result, {'data': 'test'})

    @patch('requests.get')
    def test_get_collection(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'test'}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = self.client.get_collection('collection_id')
        self.assertEqual(result, {'data': 'test'})

    @patch('requests.delete')
    def test_delete_record(self, mock_delete):
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'test'}
        mock_response.raise_for_status = MagicMock()
        mock_delete.return_value = mock_response

        result = self.client.delete_record('collection_id', 'record_id')
        self.assertEqual(result, {'data': 'test'})

    @patch('requests.get')
    def test_get_records(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'test'}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = self.client.get_records('collection_id')
        self.assertEqual(result, {'data': 'test'})

    @patch('requests.post')
    def test_create_record(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'test'}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result = self.client.create_record('collection_id', {'property': 'value'})
        self.assertEqual(result, {'data': 'test'})

    @patch('requests.post')
    def test_get_chat_response(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'test'}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result = self.client.get_chat_response('collection_id', 'message', {'key': 'value'}, 'chat_id')
        self.assertEqual(result, {'data': 'test'})

if __name__ == '__main__':
    unittest.main()