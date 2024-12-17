from itertools import batched
from math import ceil

import botocore.session
from botocore.client import BaseClient
from botocore.stub import Stubber

from explore_nwps.aws.list_objects import list_objects


class Helper:
    def __init__(self) -> None:
        # Creating a Client takes about 2 seconds, so it's much faster to create this client once
        # and re-use it for all tests!
        self.s3: BaseClient = botocore.session.get_session().create_client("s3")

    def run_test(self, object_keys: list[str], common_prefixes: list[str] = [], **kwargs) -> None:
        with self._get_s3_stubber_for_list_objects_v2(
            object_keys, common_prefixes=common_prefixes, **kwargs
        ):
            result = list_objects(self.s3, bucket="test-bucket", prefix="")
        assert result == dict(common_prefixes=common_prefixes, object_keys=object_keys)

    def _get_s3_stubber_for_list_objects_v2(
        self,
        object_keys: list[str],
        common_prefixes: list[str],
        delimiter: str = "/",
        prefix: str = "",
        bucket_name: str = "test-bucket",
        num_pages: int = 1,
    ) -> Stubber:
        """
        Args:
            num_pages: Number of `list_objects_v2` responses to add.
                The last response will have `IsTruncated` set to False.
        """
        stubber = Stubber(self.s3)
        expected_params = dict(Bucket="test-bucket", Delimiter="/", Prefix="")
        page_length = ceil(len(object_keys) / num_pages)
        for i, batched_obj_keys in enumerate(batched(object_keys, page_length)):
            response = {
                "IsTruncated": (i + 1) < num_pages,
                "Contents": [{"Key": key} for key in batched_obj_keys],
                "Name": bucket_name,
                "Prefix": prefix,
                "Delimiter": delimiter,
                "CommonPrefixes": [{"Prefix": p} for p in common_prefixes] if i == 0 else [],
                "EncodingType": "url",
                "RequestCharged": "requester",
            }
            stubber.add_response("list_objects_v2", response, expected_params)
        stubber.activate()
        return stubber


helper = Helper()


def test_list_objects_no_common_prefixes() -> None:
    helper.run_test(object_keys=["test.txt"])


def test_list_objects_1_common_prefix() -> None:
    helper.run_test(object_keys=["foo/test.txt", "foo/bar.txt"], common_prefixes=["foo/"])


def test_list_objects_1_common_prefix_2_pages() -> None:
    helper.run_test(
        object_keys=["foo/test.txt", "foo/bar.txt", "baz/", "baz/bleh.txt"],
        common_prefixes=["foo/", "baz/"],
        num_pages=2,
    )
