"""
    Delphix DCT API

    Delphix DCT API  # noqa: E501

    The version of the OpenAPI document: 3.15.0
    Contact: support@delphix.com
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import delphix.api.gateway
from delphix.api.gateway.model.effective_scope import EffectiveScope
from delphix.api.gateway.model.tag import Tag
globals()['EffectiveScope'] = EffectiveScope
globals()['Tag'] = Tag
from delphix.api.gateway.model.account import Account


class TestAccount(unittest.TestCase):
    """Account unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testAccount(self):
        """Test Account"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Account()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
