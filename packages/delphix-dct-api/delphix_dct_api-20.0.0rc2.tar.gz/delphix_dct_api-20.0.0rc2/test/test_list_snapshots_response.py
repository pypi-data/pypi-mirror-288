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
from delphix.api.gateway.model.paginated_response_metadata import PaginatedResponseMetadata
from delphix.api.gateway.model.snapshot import Snapshot
globals()['PaginatedResponseMetadata'] = PaginatedResponseMetadata
globals()['Snapshot'] = Snapshot
from delphix.api.gateway.model.list_snapshots_response import ListSnapshotsResponse


class TestListSnapshotsResponse(unittest.TestCase):
    """ListSnapshotsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testListSnapshotsResponse(self):
        """Test ListSnapshotsResponse"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ListSnapshotsResponse()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
