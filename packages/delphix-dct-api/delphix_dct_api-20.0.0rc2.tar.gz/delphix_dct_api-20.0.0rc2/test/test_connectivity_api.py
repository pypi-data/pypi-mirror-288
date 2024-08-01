"""
    Delphix DCT API

    Delphix DCT API  # noqa: E501

    The version of the OpenAPI document: 3.15.0
    Contact: support@delphix.com
    Generated by: https://openapi-generator.tech
"""


import unittest

import delphix.api.gateway
from delphix.api.gateway.api.connectivity_api import ConnectivityApi  # noqa: E501


class TestConnectivityApi(unittest.TestCase):
    """ConnectivityApi unit test stubs"""

    def setUp(self):
        self.api = ConnectivityApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_commvault_connectivity_check(self):
        """Test case for commvault_connectivity_check

        Tests whether the CommServe host is accessible from the given environment and Commvault agent.  # noqa: E501
        """
        pass

    def test_connectivity_check(self):
        """Test case for connectivity_check

        Checks connectivity between an engine and a remote host machine on a given port.  # noqa: E501
        """
        pass

    def test_database_connectivity_check(self):
        """Test case for database_connectivity_check

        Tests the validity of the supplied database credentials, returning an error if unable to connect to the database.  # noqa: E501
        """
        pass

    def test_netbackup_connectivity_check(self):
        """Test case for netbackup_connectivity_check

        Checks whether the specified NetBackup master server and client are able to communicate on the given environment.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
