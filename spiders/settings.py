import os
import MySQLdb

send_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9"}
conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='zqh', passwd='244325', db='ShuWu', charset='utf8')
cur = conn.cursor()
