import re
import socket
import requests

UA = None


# 获取地址对应的经纬度坐标
def getMap(addr) -> dict:
    url = "http://api.map.baidu.com/geocoding/v3/?"  # 百度地图API接口
    para = {
        "address": addr,  # 传入地址参数
        "output": "json",
        "ak": "myv6ZSUbM7bAdN3lKt4wGteYZA3noEZi"  # 百度地图开放平台申请ak
    }
    req = requests.get(url, para)
    req = req.json()
    return req['result']['location']


# 获取自身ip
def getMyIp():
    return re.search('\d+\.\d+\.\d+\.\d+', requests.get('http://pv.sohu.com/cityjson').text).group()


# 获得随机头
def getFakeUserAgent():
    import subprocess
    try:
        from anole import UserAgent
    except ModuleNotFoundError:
        subprocess.check_call(['pip','install', "anole"])
        from anole import UserAgent

    global UA
    if UA is None: UA = UserAgent()
    return str(UA.random)


# 获取本机ip
def getLocalIp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip
