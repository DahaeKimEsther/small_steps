from langchain.agents import tool
import os
import urllib.request
from dotenv import load_dotenv
load_dotenv('./projects/.env')


client_id = os.getenv('NAVER_CLIENT_ID')
client_secret = os.getenv("NAVER_CLIENT_SECRET")

@tool
def naver_news(search_word:str, display:int=3) -> dict:
    """Search news by search word"""
    encText = urllib.parse.quote(search_word)
    url = "https://openapi.naver.com/v1/search/news.json?query=" + encText + f"&display={display}&sort=sim"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        result = response_body.decode('utf-8')
        return result
    else:
        raise Exception(rescode)

@tool
def naver_dict(search_word:str, display:int=3) -> dict:
    """Search terms in dictionary"""
    encText = urllib.parse.quote(search_word)
    url = "https://openapi.naver.com/v1/search/encyc.json?query=" + encText + f"&display={display}"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        result = response_body.decode('utf-8')
        return result
    else:
        raise Exception(rescode)