from fastapi import FastAPI,Depends
from .routers import users,base,collect,public
from fastapi.middleware.cors import CORSMiddleware
import json
from .config import WEB_IP,WEB_PORT


app = FastAPI()
app.include_router(base.router)
app.include_router(users.router)
app.include_router(collect.router)
app.include_router(public.router)



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

#demo
@app.get('/')
def demo():
    return {'code':0,'message':"ok"}