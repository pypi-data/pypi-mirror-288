"""
    Delphix DCT API

    Delphix DCT API  # noqa: E501

    The version of the OpenAPI document: 3.15.0
    Contact: support@delphix.com
    Generated by: https://openapi-generator.tech
"""


import unittest

import delphix.api.gateway
from delphix.api.gateway.api.virtualization_jobs_api import VirtualizationJobsApi  # noqa: E501


class TestVirtualizationJobsApi(unittest.TestCase):
    """VirtualizationJobsApi unit test stubs"""

    def setUp(self):
        self.api = VirtualizationJobsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_virtualization_job_history(self):
        """Test case for get_virtualization_job_history

        Fetch a list of all virtualization jobs  # noqa: E501
        """
        pass

    def test_search_virtualization_job_history(self):
        """Test case for search_virtualization_job_history

        Search virtualization jobs  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
