import boto3
from .base import Base
from pydantic import BaseModel

s3 = boto3.client("s3")
MB = 1024 * 1024

class Input(BaseModel):
    bucket: str
    key: str
    chunk_bytes: int


class S3(Base):
    def __init__(self, bucket, key, chunk_bytes=50 * MB, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input = Input(bucket=bucket, key=key, chunk_bytes=chunk_bytes)


    def get_s3_file_size(self) -> int:
        file_size = 0
        response = s3.head_object(Bucket=self.input.bucket, Key=self.input.key)
        if response:
            file_size = int(response.get('ContentLength'))
        return file_size


    def gen(self):
        file_size = self.get_s3_file_size()
        option = {
            "Bucket": self.input.bucket,
            "Key": self.input.key,
            "ExpressionType": 'SQL',
            "Expression": 'SELECT * FROM S3Object ',
            "OutputSerialization": {
                'JSON': {
                    'RecordDelimiter': '\n'
                }
            }
        }
        is_compressed = self.input.key.endswith("gz")
        option["InputSerialization"] = {
            "CompressionType": "GZIP" if is_compressed else "NONE",
        }
        if self.input.key.strip(".gz").endswith(".csv"):
            option["InputSerialization"]["CSV"] = {
                "FileHeaderInfo": "USE",
                "FieldDelimiter": ",",
                "RecordDelimiter": "\n"
            }
        elif self.input.key.strip(".gz").endswith(".jsonl"):
            option["InputSerialization"]["JSON"] = {
                "Type": "LINES"
            }

        for start in range(0, file_size, self.input.chunk_bytes):
            end = min(start + self.input.chunk_bytes, file_size)
            if not is_compressed:
                option["ScanRange"] = {'Start': start, 'End': end}
            response = s3.select_object_content(**option)
            result = b""
            for event in response['Payload']:
                if records := event.get('Records'):
                    result += records['Payload']

            import json
            yield from map(json.loads, result.decode('utf-8').strip().split("\n"))