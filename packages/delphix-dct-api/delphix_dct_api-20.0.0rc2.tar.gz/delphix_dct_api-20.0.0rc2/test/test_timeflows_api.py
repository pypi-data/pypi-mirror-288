"""
    Delphix DCT API

    Delphix DCT API  # noqa: E501

    The version of the OpenAPI document: 3.15.0
    Contact: support@delphix.com
    Generated by: https://openapi-generator.tech
"""


import unittest

import delphix.api.gateway
from delphix.api.gateway.api.timeflows_api import TimeflowsApi  # noqa: E501


class TestTimeflowsApi(unittest.TestCase):
    """TimeflowsApi unit test stubs"""

    def setUp(self):
        self.api = TimeflowsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_timeflow_tags(self):
        """Test case for create_timeflow_tags

        Create tags for a Timeflow.  # noqa: E501
        """
        pass

    def test_delete_timeflow(self):
        """Test case for delete_timeflow

        Delete a timeflow.  # noqa: E501
        """
        pass

    def test_delete_timeflow_tags(self):
        """Test case for delete_timeflow_tags

        Delete tags for a Timeflow.  # noqa: E501
        """
        pass

    def test_get_timeflow_by_id(self):
        """Test case for get_timeflow_by_id

        Get a Timeflow by ID.  # noqa: E501
        """
        pass

    def test_get_timeflow_snapshot_day_range(self):
        """Test case for get_timeflow_snapshot_day_range

        Returns the count of TimeFlow snapshots of the Timeflow aggregated by day.  # noqa: E501
        """
        pass

    def test_get_timeflow_tags(self):
        """Test case for get_timeflow_tags

        Get tags for a Timeflow.  # noqa: E501
        """
        pass

    def test_get_timeflows(self):
        """Test case for get_timeflows

        Retrieve the list of timeflows.  # noqa: E501
        """
        pass

    def test_search_timeflows(self):
        """Test case for search_timeflows

        Search timeflows.  # noqa: E501
        """
        pass

    def test_update_timeflow(self):
        """Test case for update_timeflow

        Update values of a timeflow.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
