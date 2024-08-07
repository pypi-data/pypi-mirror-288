import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import boto3
import pytest
import logging
logging.basicConfig(level=logging.INFO)
from datetime import date
from yooncloud_core.data import S3, Athena, Koreadaychart, Koreatickchart


@pytest.fixture(scope="session")
def bucket():
    BUCKET_NAME = "yooncloud-data"
    bucket = boto3.resource("s3").Bucket(BUCKET_NAME)
    yield bucket


def test_s3(bucket):
    daychart = [a for a in S3(bucket=bucket.name, key="koreadaychart/timestamp=2024-01-02/2024-01-02.csv.gz")]
    assert len(daychart) == 2786
    assert daychart[0]["name"] == "삼성전자" and daychart[0]["volume"] == "17142847"
    assert daychart[-1]["name"]=="디에스앤엘" and daychart[-1]["volume"] == "12658080"


def test_athena():
    sql = "select * from koreadaychart where timestamp >= '2024-01-02' and timestamp <= '2024-01-05' ORDER BY timestamp"
    daychart = [a for a in Athena(sql=sql)]
    assert len(daychart)==11141

    daychart = [a for a in daychart if a["name"]=="삼성전자"]
    assert daychart[0]["date"] == "2024-01-02" and daychart[0]["volume"] == "17142847"
    assert daychart[1]["date"] == "2024-01-03" and daychart[1]["volume"] == "21753644"
    assert daychart[2]["date"] == "2024-01-04" and daychart[2]["volume"] == "15324439"
    assert daychart[3]["date"] == "2024-01-05" and daychart[3]["volume"] == "11304316"


def test_koreadaychart():
    start = "2024-01-02"
    end = "2024-01-05"
    daychart = [a for a in Koreadaychart(start_date=start, end_date=end)]
    assert len(daychart)==11141
    
    daychart = [a for a in daychart if a.name=="SK하이닉스"]
    assert daychart[0].date == date(2024, 1, 2) and daychart[0].volume == 2147458
    assert daychart[1].date == date(2024, 1, 3) and daychart[1].volume == 3257820
    assert daychart[2].date == date(2024, 1, 4) and daychart[2].volume == 2661970
    assert daychart[3].date == date(2024, 1, 5) and daychart[3].volume == 1846781


def test_koreatickchart():
    import time
    date = "2019-02-11"
    start_time = time.time()
    tickchart = [a for a in Koreatickchart(date=date)]
    # 약 5~6분정도 걸림
    logging.info(f"it tooks {round(time.time() - start_time)} secs")
    assert len(tickchart)==5924192


def test_data_transform():
    my_filter = {
        "type": "filter",
        "scripts": [
            "return row.stockcode=='005930'",
        ]
    }
    my_map = {
        "type": "map",
        "scripts": [
            "row.홀짝 = '짝' if row.volume % 2 == 0 else '홀'",
            "return row",
        ]
    }
    my_tap = {
        "type": "tap",
        "scripts": [
            "rows.append({'message': 'This is last tick!'})",
            "return rows",
        ]
    }  
    transforms = [
        my_filter,
        my_map,
        my_tap,
    ]
    daychart = [a for a in Koreadaychart(start_date="2024-01-02", end_date="2024-01-05", transforms=transforms)]

    assert all(a.stockcode=='005930' for a in daychart[:-1])
    assert all("홀짝" in a.model_dump() for a in daychart[:-1])
    assert list(daychart[-1].keys()) == ["message"]