import hashlib
from typing import Any, TypeVar, Generic, Type

# from xml.etree.ElementTree import fromstring
from simplexml import loads
import xmltodict
from fastapi import Depends, FastAPI, Header, Response
from dotenv import load_dotenv
import os
import datetime
from pydantic import BaseModel
from starlette.requests import Request

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


T = TypeVar("T", bound=BaseModel)


class Item(BaseModel):
    ToUserName: str
    FromUserName: str
    CreateTime: str


class XmlBody(Generic[T]):
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class

    async def __call__(self, request: Request) -> T:
        if "/xml" in request.headers.get("Content-Type", ""):
            body = await request.body()
            dict_data = xmltodict.parse(body)
        else:
            dict_data = await request.json()
        return dict_data


class Wechat(BaseModel):
    signature: str
    timestamp: str
    nonce: str
    echostr: str


@app.get("/test")
def test():
    return "test111"


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
async def wechat_post(item: Item = Depends(XmlBody(Item)), header: str = Header(None)):
    print(item)
    if item["xml"]["MsgType"] == "event" and item["xml"]["Event"] == "subscribe":
        ts = datetime.datetime.now().timestamp()
        xml = f"""<xml>
  <ToUserName><![CDATA[{item["xml"]["FromUserName"]}]]></ToUserName>
  <FromUserName><![CDATA[{item["xml"]["ToUserName"]}]]></FromUserName>
  <CreateTime>{int(ts)}</CreateTime>
  <MsgType><![CDATA[text]]></MsgType>
  <Content><![CDATA[感谢你关注——雨非黑科技\n\n需要什么PDF请直接回复名字\n\n原创整理:最新，最全，高清PDF]]></Content>
</xml>"""
        return Response(content=xml, media_type="application/xml")