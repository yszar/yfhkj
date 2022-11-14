import hashlib

from fastapi import FastAPI
from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv(verbose=True)

WECHAT_TOKEN = os.getenv("WECHAT_TOKEN")

description = """
**雨非黑科技**微信公众号后端API
"""

app = FastAPI(
    title="YuFei-WeChat",
    description=description,
    version="0.1.6",
    contact={
        "name": "yszar",
        "url": "https://iamjy.com",
        "email": "yszaryszar@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://mit-license.org/",
    },
)


class Wechat(BaseModel):
    signature: str
    timestamp: str
    nonce: str
    echostr: str


@app.get("/wechat", summary="微信公众号后台验证token接口")
async def wechat_get(signature: str, timestamp: str, nonce: str, echostr: str):
    token = WECHAT_TOKEN
    temp = [token, timestamp, nonce]
    temp.sort()
    res = hashlib.sha1("".join(temp).encode("utf8")).hexdigest()
    if res == signature:
        return int(echostr)
    else:
        return {"errcode": 401, "errmsg": "access denied"}


@app.post("/wechat")
async def wechat_post(xml_str: str):
    print("print", xml_str)
    return ""
