import boto3
from enum import Enum
from typing import Optional
from datetime import date
from pydantic import BaseModel, field_validator
from .base import Base
from .s3 import S3


s3 = boto3.client("s3")

class Column(str, Enum):
    stockcode = "stockcode"
    timestamp = "timestamp"
    price = "price"
    volume = "volume"
    isBull = "isBull"
    sortKey = "sortKey"


class Input(BaseModel):
    date: date
    columns: Optional[list[Column]]

    @field_validator("date")
    @classmethod
    def validate_date(cls, v:date):
        # koreatickchart 데이터는 2018-06-01 부터 2019-02-11 까지다
        assert v.toordinal() >= date.fromisoformat("2018-06-01").toordinal(), "date' must be equal or greater than 2018-06-01"
        assert v.toordinal() <= date.fromisoformat("2019-02-12").toordinal(), "date' must be equal or less than 2019-02-11"
        return v


class Koreatickchart(Base):
    def __init__(
            self,
            date:str,
            columns=["stockcode", "timestamp", "price", "volume", "isBull", "sortKey"],
            *args,
            **kwargs,
        ):
        full_schema = {
            "stockcode": "string",
            "timestamp": "datetime",
            "price": "int",
            "volume": "int",
            "isBull": "boolean",
            "sortKey": "int",
        }
        schema = {k:v for k,v in full_schema.items() if k in columns}
        super().__init__(schema=schema, *args, **kwargs)
        self.input = Input(date=date, columns=columns)


    def gen(self):
        yield from S3(bucket="yooncloud-data", key=f"koreatickchart/{self.input.date}.jsonl")