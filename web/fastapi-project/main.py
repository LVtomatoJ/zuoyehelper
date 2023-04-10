from fastapi import FastAPI,Depends
from .routers import users,base
from fastapi.middleware.cors import CORSMiddleware
import json

#读取配置文件
with open("fastapi-project/config.json", "r", encoding="utf-8") as f:
    globalConfig = json.load(f)

app = FastAPI()
app.include_router(base.router)
app.include_router(users.router)

WEB_IP=globalConfig.get('WEB_IP')
WEB_PORT=globalConfig.get('WEB_PORT')


#跨源设置
origins = [
    # "http://localhost:5173",
    # "http://127.0.0.1:5173"
    f"http://{WEB_IP}:{WEB_PORT}"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def demo():
    return {'code':0,'message':"ok"}