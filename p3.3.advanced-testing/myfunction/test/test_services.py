import logging
import unittest
from unittest.mock import Mock, patch

import boto3

from .context import services

logging.basicConfig(
    handlers=[logging.NullHandler()]
)

# Questions:
#   - are these tests isolated? NO
#   - is source code loosely coupled? NO
#   - are these tests maintainable? NO
#   - do they really perform unittest? NO
#
# Notes:
#   - requires to mock whole hierarchy
#   - there are some hidden non-easy testable resources (boto3 seesion/client)


class IocTestCase(unittest.TestCase):

    def test_request_status(self):
        context = Mock()
        context.aws_request_id = '12-34-56'

        with patch('time.sleep'):
            result = services.request_status(context, 'sample', 'test')

        self.assertEqual(result, 'sample:TEST/12-34-56')

    def test_build_result(self):
        context = Mock()
        context.aws_request_id = '12-34-56'

        with patch('time.sleep'):
            result = services.build_result(context, 'one', {'one': 'sample'}, 'test')

        self.assertEqual(result, {'result': 'sample:TEST/12-34-56', 'yaml': '5.3'})
