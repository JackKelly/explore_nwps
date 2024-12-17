from botocore.stub import Stubber
import botocore.session
from botocore.client import BaseClient

from explore_nwps.aws.list_objects import list_objects


def get_s3_stubber_for_list_objects_v2(
    object_keys: list[str],
    common_prefixes: list[str],
    delimiter: str = "/",
    prefix: str = "",
    bucket_name: str = "test-bucket",
) -> BaseClient:
    s3 = botocore.session.get_session().create_client("s3")
    stubber = Stubber(s3)
    response = {
        "IsTruncated": False,
        "Contents": [{"Key": key} for key in object_keys],
        "Name": bucket_name,
        "Prefix": prefix,
        "Delimiter": delimiter,
        "MaxKeys": 1000,
        "CommonPrefixes": [{"Prefix": p} for p in common_prefixes],
        "EncodingType": "url",
        "RequestCharged": "requester",
    }
    expected_params = dict(Bucket="test-bucket", Delimiter="/", Prefix="")
    stubber.add_response("list_objects_v2", response, expected_params)
    stubber.activate()
    return s3


def _test_helper(object_keys: list[str], common_prefixes: list[str] = []) -> None:
    s3 = get_s3_stubber_for_list_objects_v2(object_keys, common_prefixes=common_prefixes)
    result = list_objects(s3, bucket="test-bucket", prefix="")
    assert result == dict(common_prefixes=common_prefixes, object_keys=object_keys)


def test_list_objects_no_common_prefixes() -> None:
    _test_helper(object_keys=["test.txt"])


def test_list_objects_1_common_prefix() -> None:
    _test_helper(object_keys=["foo/test.txt", "foo/bar.txt"], common_prefixes=["foo/"])
