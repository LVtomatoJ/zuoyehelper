# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
import requests
from .config import QCOS_BUCKET, QCOS_SECRET_ID, QCOS_SECRET_KEY, QCOS_REGION, QCOS_EXP, QCOS_QUEUE_ID
# import config
# 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


secret_id = QCOS_SECRET_ID
secret_key = QCOS_SECRET_KEY
bucket = QCOS_BUCKET
region = QCOS_REGION
scheme = 'https'
expired = QCOS_EXP
queue_id = QCOS_QUEUE_ID

config = CosConfig(Region=region, SecretId=secret_id,
                   SecretKey=secret_key, Scheme=scheme)
client = CosS3Client(config)


def get_upload_url(key) -> str:
    global bucket
    global expired
    url = client.get_presigned_url(
        Method='PUT',
        Bucket=bucket,
        Key=key,
        Expired=expired
    )
    return url


def qcos_check_upload_exist(key) -> bool:
    global bucket
    result = client.object_exists(
        Bucket=bucket,
        Key=key)
    return result


def qcos_add_zip_job(file, out):
    global bucket
    global queue_id
    global region
    result = client.ci_add_zip_file_job(
        bucket, file, out, queue_id, region, ContentType='application/xml')
    return result

def qcos_check_zip_job(job_id):
    global bucket
    result = client.ci_auditing_zip_query(bucket,job_id)
    return result

def get_download_url(key) -> str:
    global bucket
    global expired
    url = client.get_presigned_url(
        Method='GET',
        Bucket=bucket,
        Key=key,
        Expired=expired
    )
    return url


{'JobsDetail': 
 {'Code': 'Success', 
  'CreationTime': '2023-04-17T09:00:42+0800', 
  'EndTime': '-',
  'JobId': 'f471755d8dcbb11ed91b4f587100bac86',
  'Message': None,
  'Operation': {'FileCompressConfig': {'Flatten': '0', 'Format': 'zip', 'Prefix': '/6438233b5b41aacf93c62ac3', 'UrlList': None},
                                                                                                                                                                            'JobLevel': '0', 'Output': {'Bucket': 'zuoyehelper-1252419241', 'Object': '/6438233b5b41aacf93c62ac3/6438233b5b41aacf93c62ac3.zip', 'Region': 'ap-chengdu'}}, 'Progress': '0', 'QueueId': 'p60a9a795f75447feb41bbc583e386899', 'StartTime': '-', 'State': 'Submitted', 'Tag': 'FileCompress'}}
