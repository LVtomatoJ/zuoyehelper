from datetime import datetime
from fastapi import APIRouter,Depends
from pydantic import BaseModel
from ..dependencies import check_collect_exist,check_upload,check_upload_exist
from ..db import get_collection
from ..code import errorcode
from ..qcos import get_upload_url,qcos_check_upload_exist

router = APIRouter(prefix='/api/public',tags=['public'])

#collect need模型
class Need(BaseModel):
    index:int
    name:str

#返回collect模型
class Collect(BaseModel):
    endtime:datetime
    type:int
    title:str
    destict:str|None=None
    need:list[Need]

#获取collect内容
@router.get('/getcollect',response_model=Collect)
def get_collect(collect = Depends(check_collect_exist)):
    print(collect)
    return collect

#上传文件记录,返回上传URL
@router.post('/upload')
def upload_file(uploaddata = Depends(check_upload)):
    try:
        uploaddb = get_collection('upload')
        result = uploaddb.insert_one(uploaddata)
        collect_id = uploaddata['collect_id']
        collectdb = get_collection('collect')
        collect = collectdb.find_one({'_id':collect_id})
        user_id = collect['user_id']
        sign = get_upload_url(str(user_id)+"/"+str(collect_id)+"/"+uploaddata['filename'])
        code = 200
    except Exception as e:
        code = 305
    finally:
        if code!=200:
            return {'code':code,'message':errorcode[code]}
        else:
            return {'code':200,'message':sign,'filename':uploaddata['filename']}

@router.get('/check_upload')
def update_upload_data(upload = Depends(check_upload_exist)):
    filename = upload['filename']
    collect_id = upload['collect_id']
    collectdb = get_collection('collect')
    collect = collectdb.find_one({'_id':collect_id})
    user_id = collect['user_id']
    key = str(user_id)+"/"+str(collect_id)+'/'+filename
    if qcos_check_upload_exist(key):
        uploaddb = get_collection('upload')
        result = uploaddb.update_one({'filename':filename,'collect_id':collect_id},{"$set":{'status':1}})
        if result.modified_count!=1:
            code =  307
        else:

            code = 200
    else:
        code = 306
    return {'code':code,'message':errorcode[code]}