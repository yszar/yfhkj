import xml.etree.ElementTree as ET


x = """<xml>
    <ToUserName>
        <![CDATA[toUser]]>
    </ToUserName>
    <FromUserName>
        <![CDATA[FromUser]]>
    </FromUserName>
    <CreateTime>123456789</CreateTime>
    <MsgType>
        <![CDATA[event]]>
    </MsgType>
    <Event>
        <![CDATA[subscribe]]>
    </Event>
</xml>"""


a = ET.fromstring(x)
aa = 1