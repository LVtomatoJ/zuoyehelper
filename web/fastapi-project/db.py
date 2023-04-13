from pymongo import MongoClient
from pymongo.collection import Collection
from .config import DB_IP,DB_PORT

#创建数据库连接
client = MongoClient(DB_IP, DB_PORT)
db = client['zuoyehelper']

def get_collection(name:str) -> Collection:
    """返回对应数据库表

    Args:
        name (str): 表名

    Returns:
        Collection: 表操作对象
    """
    return db[name]