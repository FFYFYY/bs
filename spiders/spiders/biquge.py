import requests
from lxml import etree
from spiders.storage import stored_mysql
from spiders.settings import send_headers, conn, cur


def qu_la_spider():
    with open('../message/qula.txt') as f:
        a = int(f.readline())

    for i in range(a, 1000000):
        response = requests.get("https://www.qu.la/book/%s/" % str(i), headers=send_headers)
        html = etree.HTML(response.text)
        if html is None:
            print('error', i)
            with open('message/errors.txt', 'a') as f:
                f.write('qu.la\t\t' + str(i) + '\n')
            continue

        book_name = html.xpath('//*[@id="info"]/h1/text()')[0]
        author = html.xpath('//*[@id="info"]/p[1]/text()')[0].replace('作  者：', '')
        img_url = "https://www.qu.la" + html.xpath('//*[@id="fmimg"]/img/@src')[0]
        intro = html.xpath('//*[@id="intro"]/text()')[0].strip()
        if not intro:
            intro = ''

        stored_mysql(conn, cur, i, book_name, author, img_url=img_url, intro=intro)

    cur.close()
    conn.close()


if __name__ == '__main__':
    qu_la_spider()
