
from fastapi import APIRouter,Depends
from ..dependencies import check_token,get_token_username


router = APIRouter(prefix='/api/user',tags=['user'],dependencies=[Depends(check_token)])

@router.get('/info')
def get_info(username:str = Depends(get_token_username)):
    pass