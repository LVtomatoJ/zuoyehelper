from pymongo import MongoClient
from pymongo.collection import Collection
import json
with open("fastapi-project/config.json", "r", encoding="utf-8") as f:
    globalConfig = json.load(f)

client = MongoClient(globalConfig.get('DB_IP'), globalConfig.get('DB_PORT'))
db = client['zuoyehelper']

def get_collection(name:str) -> Collection:
    return db[name]