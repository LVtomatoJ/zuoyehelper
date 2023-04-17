from datetime import datetime
import pprint
from fastapi import APIRouter,Depends
from pydantic import BaseModel,constr
from ..dependencies import check_token,get_token_username,check_collect_belong_user
from ..db import get_collection
from ..code import errorcode
from ..config import WEB_IP,WEB_PORT
from ..qcos import qcos_add_zip_job,qcos_check_zip_job,get_download_url
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
    
@router.get('/make_zip')
def make_zip(collect = Depends(check_collect_belong_user)):
    #1.创建任务
    file = str(collect['_id'])+'/'
    outfile = 'zip/'+str(collect['_id'])+'.zip'
    result = qcos_add_zip_job(file=file,out=outfile)
    if result['JobsDetail']['Code']!='Success':
        code = 307
    else:
        job_id = result['JobsDetail']['JobId']
        #2.添加(更新)到数据库
        jobdb = get_collection('job')
        result = jobdb.update_one({
            'collect_id':collect['_id'],
            'job_id':job_id
        },{'$set':{'status':0}},upsert=True)
        code = 200
    return {'code':code,'message':errorcode[code]}

@router.get('/check_zip_job')
def check_zip_job(collect = Depends(check_collect_belong_user)):
    #获取job_id
    jobdb = get_collection('job')
    job = jobdb.find_one({'collect_id':collect['_id']})
    if not job:
        #job不存在
        code = 311
        return {'code':311,'message':errorcode[code]}
    job_id = job['job_id']
    #获取任务进度
    result = qcos_check_zip_job(job_id)
    if result['JobsDetail']['Code']!='Success':
        code = 308
        return {'code':code,'message':errorcode[code]}
    else:
        process = result['JobsDetail']['Progress']
        #如果100则更新数据库
        result = jobdb.update_one({
            'job_id':job_id
        },{'$set':{'status':1}},upsert=True)
        return {'code':200,'message':process}

@router.get('/get_zip')
def get_zip(collect = Depends(check_collect_belong_user)):
    #判断job状态
    jobdb = get_collection('job')
    job = jobdb.find_one({'collect_id':collect['_id']})
    status = job['status']
    if status==0:
        code = 309
        return {'code':309,'message':errorcode[code]}
    else:
        #获取url
        key = 'zip/'+str(collect['_id'])+'.zip'
        url = get_download_url(key)
        return {'code':200,'message':url}

@router.get('/stop')
def stop_collect(collect = Depends(check_collect_belong_user)):
    try:
        #将collect endtime更新为当前时间（收集结束）
        collectdb = get_collection('collect')
        result = collectdb.update_one({'_id':collect['_id']},{'$set':{'endtime':datetime.now()}})
        #创建压缩任务
        #1.创建任务
        file = str(collect['_id'])+'/'
        outfile = 'zip/'+str(collect['_id'])+'.zip'
        result = qcos_add_zip_job(file=file,out=outfile)
        if result['JobsDetail']['Code']!='Success':
            code = 307
        else:
            job_id = result['JobsDetail']['JobId']
            #2.添加(更新)到数据库
            jobdb = get_collection('job')
            result = jobdb.update_one({
                'collect_id':collect['_id'],
                'job_id':job_id
            },{'$set':{'status':0}},upsert=True)
            code = 200
    except Exception as e:
        code=310
    finally:
        return {'code':code,'message':errorcode[code]}
    
