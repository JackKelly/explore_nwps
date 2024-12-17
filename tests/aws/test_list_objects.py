from botocore.stub import Stubber
import botocore.session
from botocore.client import BaseClient
from itertools import batched
from math import ceil

from explore_nwps.aws.list_objects import list_objects


s3 = botocore.session.get_session().create_client("s3")
stubber = Stubber(s3)


def get_s3_stubber_for_list_objects_v2(
    object_keys: list[str],
    common_prefixes: list[str],
    delimiter: str = "/",
    prefix: str = "",
    bucket_name: str = "test-bucket",
    num_pages: int = 1,
) -> BaseClient:
    """
    Args:
        num_pages: Number of `list_objects_v2` responses to add.
            The last response will have `IsTruncated` set to False.
    """
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
    return s3


def _test_helper(object_keys: list[str], common_prefixes: list[str] = [], **kwargs) -> None:
    s3 = get_s3_stubber_for_list_objects_v2(object_keys, common_prefixes=common_prefixes, **kwargs)
    result = list_objects(s3, bucket="test-bucket", prefix="")
    assert result == dict(common_prefixes=common_prefixes, object_keys=object_keys)


def test_list_objects_no_common_prefixes() -> None:
    _test_helper(object_keys=["test.txt"])


def test_list_objects_1_common_prefix() -> None:
    _test_helper(object_keys=["foo/test.txt", "foo/bar.txt"], common_prefixes=["foo/"])


def test_list_objects_1_common_prefix_2_pages() -> None:
    _test_helper(
        object_keys=["foo/test.txt", "foo/bar.txt", "baz/", "baz/bleh.txt"],
        common_prefixes=["foo/", "baz/"],
        num_pages=2,
    )
