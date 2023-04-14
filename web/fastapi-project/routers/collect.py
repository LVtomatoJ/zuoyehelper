from datetime import datetime
import pprint
from fastapi import APIRouter,Depends
from pydantic import BaseModel,constr
from ..dependencies import check_token,get_token_username
from ..db import get_collection
from ..code import errorcode
from ..config import WEB_IP,WEB_PORT

#解决返回objectid报错问题
from bson.objectid import ObjectId
import pydantic
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str


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
        inserted_id = collectdb.insert_one(data).inserted_id
        code = 200
    except Exception:
        code = 304
    finally:
        if code!=200:
            return {'code':code,'message':errorcode[code]}
        else:
            return {'code':200,'message':f'http://'+WEB_IP+':'+str(WEB_PORT)+"/"+"public/collect"+'/'+str(inserted_id)}
        
@router.get('/get')
def get_collects(page:int,limit:int,username:str = Depends(get_token_username)):
    #获取user_id
    userdb = get_collection('user')
    user_id = userdb.find_one({'username':username})['_id']
    #获取collects
    collectdb = get_collection('collect')
    skip = (page-1)*limit
    collects = collectdb.find({'user_id':user_id}).skip(skip).limit(limit)
    data = [item for item in collects]
    return {'code':200,'message':data}

@router.get('/total')
def get_collect_total(username:str = Depends(get_token_username)):
    
    #获取user_id
    userdb = get_collection('user')
    user_id = userdb.find_one({'username':username})['_id']
    #获取collects
    collectdb = get_collection('collect')
    total = collectdb.count_documents({'user_id':user_id})
    return {'code':200,'message':total}
    

