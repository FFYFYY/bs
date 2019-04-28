import MySQLdb
import requests


send_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9"}

proxies = {'http':'http://117.93.81.90:53281'}

def get_response(url, charset='utf-8'):
    response = requests.get(url, headers=send_headers, proxies=proxies)
    response.encoding = charset
    return response


conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='zqh', passwd='test123', db='ShuWu', charset='utf8')
cur = conn.cursor()
