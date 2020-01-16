import unittest
from unittest.mock import patch

from .context import di, ioc


class IocTestCase(unittest.TestCase):

    def test_no_params(self):
        with self.assertRaises(di.IocContainer.Error) as ctx:
            ioc.get_container()

        self.assertIn('mandatory parameter is not provided', str(ctx.exception))

    def test_valid_container(self):
        container = ioc.get_container(
            code='my_str',
            ns_dict={'key': 'value'},
        )

        self.assertIsInstance(container, di.IocContainer)
