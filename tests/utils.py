import datetime
from typing import List
import json


def read_posts_dicts(filename: str) -> List[dict]:
    with open(filename, encoding='utf8') as f:
        post_dicts = json.load(f)
    for post_dict in post_dicts:
        post_dict['_id'] = post_dict['_id']['$oid']
        post_dict['created'] = read_date_from_str(post_dict['created']['$date'])
    return post_dicts


def read_post_dict(filename: str) -> dict:
    with open(filename, encoding='utf8') as f:
        post_dict = json.load(f)
    post_dict['_id'] = post_dict['_id']['$oid']
    post_dict['created'] = read_date_from_str(post_dict['created']['$date'])
    return post_dict


def read_date_from_str(data_str: str) -> datetime:
    return datetime.datetime.strptime(data_str,'%Y-%m-%dT%H:%M:%S.%fZ')