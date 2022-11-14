import hashlib

from fastapi import FastAPI
from dotenv import load_dotenv
import os


load_dotenv(verbose=True)

WECHAT_TOKEN = os.getenv("WECHAT_TOKEN")


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/wechat")
async def hello_wechat(signature: str, timestamp: str, nonce: str, echostr: str):
    token = WECHAT_TOKEN
    temp = [token, timestamp, nonce]
    temp.sort()
    res = hashlib.sha1("".join(temp).encode("utf8")).hexdigest()
    if res == signature:
        return int(echostr)
    else:
        return {"errcode": 401, "errmsg": "access denied"}
