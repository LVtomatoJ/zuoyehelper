from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import APIRouter,Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from ..db import get_collection
from pymongo.collection import Collection
import json
from passlib.context import CryptContext

#密码hash对象
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#对比密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#密码hash
def get_password_hash(password):
    return pwd_context.hash(password)

#获取全局配置文件
with open("fastapi-project/config.json", "r", encoding="utf-8") as f:
    globalConfig = json.load(f)
SECRET_KEY = globalConfig.get('SECRET_KEY')
ALGORITHM = globalConfig.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = globalConfig.get('ACCESS_TOKEN_EXPIRE_MINUTES')

#模型
class Token(BaseModel):
    access_token: str
    token_type: str

class Reg(BaseModel):
    code: str
    message: str

class RegInfo(BaseModel):
    username: str
    password: str


def create_access_token(data: dict, expires_delta: timedelta|None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# def check_password(username:str,password:str):
#     userdb = get_collection('user')
#     userdb.find_one({'username':username})

router = APIRouter(tags=['base'])

@router.post('/token')
def login(from_token:OAuth2PasswordRequestForm=Depends()):
    username = from_token.username
    password = from_token.password
    userdb = get_collection('user')
    user = userdb.find_one({'username':username})
    if not user:
        return {'code':303,'message':"用户不存在"}
    else:
        if verify_password(password,user['password']):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
            return {'code':200,"access_token": access_token, "token_type": "bearer"}
        else:
            return {'code':301,'message':'密码错误'}
    
@router.post('/reg')
def reg(reginfo:RegInfo):
    username = reginfo.username
    password = get_password_hash(reginfo.password)
    userdb = get_collection('user')
    if userdb.find_one({'username':username}):
        return {'code':302,'message':"用户已存在"}
    else:
        anser = userdb.insert_one({'username':username,'password':password})
        return {'code':200,'message':"注册成功"}