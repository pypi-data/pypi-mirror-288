import boto3
import tarfile, json
from io import BytesIO

s3 = boto3.client('s3')
lambda_client = boto3.client('lambda')

def open_content(bucket_name, file_key, filter_map=None):
  streamContents = s3.get_object(Bucket=bucket_name, Key=file_key)['Body']
  file_content = streamContents.read()
  with tarfile.open(fileobj=BytesIO(file_content), mode="r:gz") as tar:
    for file_info in tar.getmembers():
      if file_info.name.endswith('.json'):
        file_in_tar = tar.extractfile(file_info)
        for line in file_in_tar:
          obj = json.loads(line.decode('utf-8'))
          if filter(obj, filter_map):
            yield obj


def filter(obj, filter_map=None):
  if filter_map is not None:
    for key in filter_map:
      if obj.get(key) == filter_map[key]:
        return True
    return False
  return True
