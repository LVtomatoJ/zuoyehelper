from datetime import datetime
import random
import string
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
import json

from pydantic import BaseModel
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from pymongo.collection import Collection
from .db import get_collection
from bson.objectid import ObjectId
from pymongo.typings import _DocumentType

# bcrypt加密验证对象
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauto依赖
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def check_token(token: str = Depends(oauth2_scheme)):
    """验证请求中token是否存在是否正确，无返回值,失败抛出401

    Args:
        token (str, optional): _description_. Defaults to Depends(oauth2_scheme).

    Raises:
        credentials_exception: _description_
        credentials_exception: _description_
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception


def get_token_username(token: str = Depends(oauth2_scheme)) -> str:
    """不验证token是否正确,仅返回token中包含的username

    Args:
        token (str, optional): _description_. Defaults to Depends(oauth2_scheme).

    Returns:
        str: token中包含的username
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    return username


def check_collect_exist(collection_id: str) -> _DocumentType:
    try:
        collectdb: Collection = get_collection('collect')
        result: _DocumentType = collectdb.find_one(
            {'_id': ObjectId(collection_id)}
            )
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="收集表不存在"
        )
#collect need模型
class UploadData(dict):
    index:int
    name:str
    value:str

class Upload(BaseModel):
    data:list[UploadData]
    filename:str

def check_upload(formdata:Upload,collect:_DocumentType=Depends(check_collect_exist)):
    #检查data格式
    need = collect.get('need')
    need = sorted(need,key=lambda a: a['index'])
    data = sorted(formdata.data,key=lambda a: a['index'])
    flag = True
    if(len(need)==len(data)):
        for i in range(len(need)):
            if need[i]['name']!=data[i]['name']:
                flag=False
                break
    else:
        flag=False
    if not flag:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="收集表数据错误"
        )
    result = dict()

    #获取filename
    if len(need)==0:
        #生成随机五位字符串文件名
        filename = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
    else:
        values:list = [ a['value'] for a in data]
        filename='-'.join(values)
    #添加后缀
    filename+='.'
    filename+=formdata.filename.split('.')[-1]
    result['filename'] = filename

    #添加其余属性
    result['uptime'] = datetime.utcnow()
    result['collect_id'] = collect['_id']
    result['data'] = data
    result['status'] = 0
    return result