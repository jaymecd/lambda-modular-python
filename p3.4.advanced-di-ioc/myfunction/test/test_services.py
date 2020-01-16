import logging
import unittest
from unittest.mock import Mock, patch

from .context import services

logging.basicConfig(
    handlers=[logging.NullHandler()]
)


class IocTestCase(unittest.TestCase):

    def test_status_requester(self):
        mock_boto3 = Mock()

        mock_context = Mock()
        mock_context.aws_request_id = '12-34-56'

        sut = services.status_requester(mock_boto3, mock_context, 'test')

        with patch('time.sleep'):
            result = sut('sample')

        mock_boto3.client.assert_called_once_with('ssm')
        self.assertEqual(result, 'sample:TEST/12-34-56')

    def test_result_builder(self):

        def request_status(arg):
            return {'one': arg}

        sut = services.result_builder(request_status, {'test': 'fest'})

        result = sut('test')

        self.assertIn('result', result)
        self.assertEqual(result['result'], {'one': 'fest'})

    def test_direct_handler(self):

        def build_result(arg):
            return {'two': arg}

        sut = services.direct_handler(build_result)

        result = sut({'key': 'test'})

        self.assertEqual(result, {'two': 'test'})
