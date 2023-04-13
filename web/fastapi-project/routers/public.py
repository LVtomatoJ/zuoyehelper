from datetime import datetime
from fastapi import APIRouter,Depends
from pydantic import BaseModel
from ..dependencies import check_collect_exist,check_upload
from ..db import get_collection
from ..code import errorcode
from ..qcos import get_upload_url

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
def uploadfile(upload = Depends(check_upload)):
    try:
        uploaddb = get_collection('upload')
        result = uploaddb.insert_one(upload)
        sign = get_upload_url(str(upload['collect_id'])+"/"+upload['filename'])
        code = 200
    except Exception as e:
        code = 305
    finally:
        if code!=200:
            return {'code':code,'message':errorcode[code]}
        else:
            return {'code':200,'message':sign}