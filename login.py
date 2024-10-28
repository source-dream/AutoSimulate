# 量化平台登录模块
import requests
import json
from os.path import expanduser
from typing import Optional
from requests.auth import HTTPBasicAuth
from config import BASE_URL, USERNAME, PASSWORD

def login() -> tuple[Optional[requests.Session], Optional[str]]:
    """
    登录Brain平台

    args:
        None

    returns:
        sess: requests.Session, 登录成功时返回的会话对象
        err: str, 登录失败时返回的错误信息
    """
    sess = requests.Session()
    sess.auth = HTTPBasicAuth(USERNAME, PASSWORD)
    if not USERNAME or not PASSWORD or not BASE_URL:
        return None, "请配置config.py文件"
    response = sess.post(f'{BASE_URL}/authentication')
    if response.status_code != 201:
        return None, "登录失败"
    return sess, None