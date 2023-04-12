# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
import requests
from .config import QCOS_BUCKET,QCOS_SECRET_ID,QCOS_SECRET_KEY,QCOS_REGION,QCOS_EXP
# import config
# 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


secret_id = QCOS_SECRET_ID
secret_key = QCOS_SECRET_KEY
bucket = QCOS_BUCKET
region = QCOS_REGION
scheme = 'https'
expired = QCOS_EXP

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Scheme=scheme)
client = CosS3Client(config)


def get_upload_url(key):
    global bucket
    global expired
    url = client.get_presigned_url(
        Method='PUT',
        Bucket=bucket,
        Key=key,
        Expired=expired
    )
    return url