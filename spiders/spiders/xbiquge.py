import requests
from lxml import etree
from spiders.storage import stored_books
from spiders.settings import send_headers, conn, cur


def get_all_urls():
    response = requests.get("http://www.xbiquge.la/xiaoshuodaquan/", headers=send_headers)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    all_urls = html.xpath('//*[@id="main"]//a/@href')
    return all_urls


def xbiquge_spider():
    with open('../message/xbiquge.txt') as f:
        a = int(f.readline())
    response = requests.get('http://www.xbiquge.la/', headers=send_headers)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    b = int(html.xpath('//*[@id="newscontent"]/div[2]/ul/li[1]/span[2]/a/@href')[0].split('/')[-2])

    for i in range(a,b):
        response = requests.get('http://www.xbiquge.la/1/%s/' % str(i), headers=send_headers)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        if response.status_code == 200:
            book_name = html.xpath('//*[@id="info"]/h1/text()')[0]
            author = html.xpath('//*[@id="info"]/p[1]/text()')[0].replace('作\xa0\xa0\xa0\xa0者：', '').strip()
            intro = html.xpath('//*[@id="intro"]/p[2]/text()')
            if intro:
                intro = intro[0].replace(' ', '').replace('\n', '').replace('\r', '')
            else:
                intro = ''
            img_url = html.xpath('//*[@id="fmimg"]/img/@src')[0]
            stored_books(conn, cur, book_name, author, book_url=response.url, img_url=img_url, intro=intro)
            with open('../message/xbiquge.txt', 'w') as f:
                f.write(str(i))
        else:
            with open('../message/errors.txt', 'a') as f:
                f.write(response.url + '\n')
            continue


if __name__ == '__main__':
    xbiquge_spider()
    conn.close()
    cur.close()
