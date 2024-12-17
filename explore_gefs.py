import marimo

__generated_with = "0.10.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import boto3
    import marimo as mo
    from botocore import UNSIGNED
    from botocore.client import Config

    return Config, UNSIGNED, boto3, mo


@app.cell
def _(Config, Final, UNSIGNED, boto3):
    BUCKET: Final[str] = "noaa-gefs-pds"

    client = boto3.client("s3", config=Config(signature_version=UNSIGNED))
    return BUCKET, client


@app.cell
def _(botocore):
    def _list_objects_without_auto_continuation(
        client: botocore.client.S3, bucket: str, prefix: str, continuation_token=""
    ) -> dict[str, object]:
        kwargs = {}
        if continuation_token:
            kwargs["ContinuationToken"] = continuation_token
        response = client.list_objects_v2(
            Bucket=bucket, Delimiter="/", Prefix=prefix, **kwargs
        )
        print("BAR")
        return {
            "is_truncated": response.get("IsTruncated", False),
            "common_prefixes": [
                item["Prefix"] for item in response.get("CommonPrefixes", [])
            ],
            "objects": [object["Key"] for object in response.get("Contents", [])],
            "continuation_token": response.get("NextContinuationToken"),
        }

    # List objects with automatic continuation.
    def list_objects(
        client: botocore.client.S3, bucket: str, prefix: str
    ) -> dict[str, list]:
        response = _list_objects_without_auto_continuation(client, bucket, prefix)
        output = {
            "common_prefixes": response["common_prefixes"],
            "objects": response["objects"],
        }
        while response["is_truncated"]:
            response = _list_objects_without_auto_continuation(
                client, bucket, prefix, response["continuation_token"]
            )
            output["common_prefixes"].extend(response["common_prefixes"])
            output["objects"].extend(response["objects"])
        return output

    return (list_objects,)


@app.cell
def _(client):
    type(client)
    return


@app.cell
def _(BUCKET, client, list_objects):
    list_objects(client, bucket=BUCKET, prefix="gefs.20241210/")
    return


@app.cell
def _(BUCKET, client, list_objects):
    list_objects(client, bucket=BUCKET, prefix="gefs.20241210/00/")
    return


@app.cell
def _(client, list_objects):
    list_objects(client, bucket="noaa-gefs-pds", prefix="gefs.20241210/00/atmos/")
    return


@app.cell
def _(client, list_objects):
    list_obj = list_objects(
        client, bucket="noaa-gefs-pds", prefix="gefs.20241210/06/atmos/pgrb2ap5/"
    )
    return (list_obj,)


@app.cell
def _(list_obj):
    filenames = [filename.split("/")[-1] for filename in list_obj["objects"]]
    return (filenames,)


@app.cell
def _(filenames):
    unique_parts = []
    for filename in filenames:
        sections = filename.split(".")
        for i, section in enumerate(sections):
            try:
                s = unique_parts[i]
            except IndexError:
                unique_parts.append(set())
                s = unique_parts[i]
            s.add(section)

    for i, unique_part in enumerate(unique_parts):
        unique_parts[i] = list(unique_part)
        unique_parts[i].sort()
    return filename, i, s, section, sections, unique_part, unique_parts


@app.cell
def _(unique_parts):
    unique_parts
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
