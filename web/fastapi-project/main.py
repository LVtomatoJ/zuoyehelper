from fastapi import FastAPI,Depends
from .routers import users,base
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(base.router)
app.include_router(users.router)



origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)