import requests
from lxml import etree
from spiders.settings import send_headers


def get_all_urls():
    response = requests.get("http://www.xbiquge.la/xiaoshuodaquan/", headers=send_headers,timeout=(3, 10))
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    all_urls = html.xpath('//*[@id="main"]//a/@href')
    return all_urls


def get_novel_msg(url):
    response = requests.get(url, headers=send_headers, timeout=(3, 10))
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    book_name = html.xpath('//*[@id="info"]/h1/text()')[0]
    author = html.xpath('//*[@id="info"]/p[1]/text()')[0].replace('作\xa0\xa0\xa0\xa0者：', '')
    intro = html.xpath('//*[@id="intro"]/p[2]/text()')[0].replace(' ', '').replace('\n', '').replace('\r', '')
    print(book_name, author, intro, '\n')


if __name__ == '__main__':
    book_urls = get_all_urls()
    for i in book_urls[:10]:
        get_novel_msg(i)
