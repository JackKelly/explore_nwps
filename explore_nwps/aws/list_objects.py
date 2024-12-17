from typing import Any, Optional

from botocore.client import BaseClient


def _list_objects_without_auto_continuation(
    client: BaseClient,
    bucket: str,
    prefix: str,
    continuation_token: Optional[str] = None,
) -> dict[str, Any]:
    kwargs: dict[str, str] = dict(Bucket=bucket, Delimiter="/", Prefix=prefix)
    if continuation_token:
        kwargs["ContinuationToken"] = continuation_token
    response = client.list_objects_v2(**kwargs)
    return {
        "is_truncated": response.get("IsTruncated", False),
        "common_prefixes": [item["Prefix"] for item in response.get("CommonPrefixes", [])],
        "object_keys": [object["Key"] for object in response.get("Contents", [])],
        "continuation_token": response.get("NextContinuationToken"),
    }


def list_objects(client: BaseClient, bucket: str, prefix: str) -> dict[str, list]:
    """List objects with automatic continuation."""
    response = _list_objects_without_auto_continuation(client, bucket, prefix)
    output = {
        "common_prefixes": response["common_prefixes"],
        "object_keys": response["object_keys"],
    }
    while response["is_truncated"]:
        response = _list_objects_without_auto_continuation(
            client, bucket, prefix, response["continuation_token"]
        )
        output["common_prefixes"].extend(response["common_prefixes"])
        output["object_keys"].extend(response["object_keys"])
    return output
