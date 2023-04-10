from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError,jwt
import json
from .config import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES

#bcrypt加密验证对象
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#oauto依赖
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
    
def get_token_username(token: str = Depends(oauth2_scheme))->str:
    """不验证token是否正确,仅返回token中包含的username

    Args:
        token (str, optional): _description_. Defaults to Depends(oauth2_scheme).

    Returns:
        str: token中包含的username
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    return username