from datetime import datetime
from fastapi import APIRouter,Depends
from pydantic import BaseModel,constr
from bson.objectid import ObjectId
from ..dependencies import check_token,get_token_username
from ..db import get_collection
from ..code import errorcode

router = APIRouter(prefix='/api/collect',tags=['collect'],dependencies=[Depends(check_token)])

#collect need模型
class Need(BaseModel):
    index:int
    name:str


#接收collect模型
class Collect(BaseModel):
    endtime:datetime
    type:int
    title:str
    destict:str|None=None
    need:list[Need]


@router.post('/add')
def add_collect(collect:Collect,username:str = Depends(get_token_username)):
    try:
        #获取user_id
        userdb = get_collection('user')
        user_id:ObjectId = userdb.find_one({'username':username}).get('_id')
        #添加到collect表
        collectdb = get_collection('collect')
        data = collect.dict()
        data['user_id'] = user_id
        inserted_id = collectdb.insert_one(data)
        code = 200
    except Exception:
        code = 304
    finally:
        return {'code':code,'message':errorcode[code]}
    

