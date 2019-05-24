import requests
from lxml import etree
from spiders.storage import stored_books
from spiders.settings import send_headers, conn, cur


def qu_la_spider():
    with open('../message/qula.txt') as f:
        a = int(f.readline())
    response = requests.get('https://www.qu.la/', headers=send_headers)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    b = int(html.xpath('//*[@id="newscontent"]/div[2]/ul/li[1]/span[2]/a/@href')[0].split('/')[2])

    for i in range(a, b):
        response = requests.get("https://www.qu.la/book/%s/" % str(i), headers=send_headers)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        if html is not None:
            book_name = html.xpath('//*[@id="info"]/h1/text()')[0].strip()
            author = html.xpath('//*[@id="info"]/p[1]/text()')[0].replace('作  者：', '').strip()
            img_url = "https://www.qu.la" + html.xpath('//*[@id="fmimg"]/img/@src')[0]
            intro = html.xpath('//*[@id="intro"]/text()')[0].strip()
            intro = intro if intro else None
            stored_books(conn, cur, book_name, author, book_url=response.url, img_url=img_url, intro=intro)
            with open('../message/qula.txt', 'w') as f:
                f.write(str(i))
        else:
            with open('../message/errors.txt', 'a') as f:
                f.write(response.url + '\n')
            continue


if __name__ == '__main__':
    qu_la_spider()
    conn.close()
    cur.close()
