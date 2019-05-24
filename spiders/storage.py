import os


def stored_books(conn, cur, book_name, author, book_url='', intro='', img_url='', category=''):
    cur.execute("select * from books where book_name='%s' and author='%s' limit 1" %
                (book_name, author))
    is_book_stored = cur.fetchone()
    if not is_book_stored:
        try:
            cur.execute(
                "insert into books(book_name, author, intro, img_url, category) values('%s', '%s', '%s', '%s', '%s')"
                % (book_name, author, intro, img_url, category))
            conn.commit()
        except Exception as e:
            print("%s保存失败：" % book_url, e)
            conn.rollback()
            os.exit(0)
        else:
            print(book_name, "*************************", "保存成功")
            cur.execute("select id from books order by id desc limit 1")
            book_id = cur.fetchone()[0]
            try:
                cur.execute("insert into book_urls(book_url, book_id) values('%s', '%s')" % (
                    book_url, book_id))
                conn.commit()
            except Exception as e:
                print(e)
                conn.rollback()
                os.exit(0)
    else:
        print(book_url,'该书已存在！')
        cur.execute(
            "select id from book_urls where book_url='%s' limit 1" % book_url)
        is_book_url_stored = cur.fetchone()
        try:
            if is_book_stored[3] == '' and intro:
                cur.execute("update books set intro='%s' where id=%d" %
                            (intro, is_book_stored[0]))

            if is_book_stored[4] == '' and img_url:
                cur.execute("update books set img_url='%s' where id=%d" %
                            (img_url, is_book_stored[0]))

            if is_book_stored[5] == '' and category:
                cur.execute("update books set category='%s' where id=%d" %
                            (category, is_book_stored[0]))

            if not is_book_url_stored:
                cur.execute(
                    "insert into book_urls(book_url, book_id) values('%s', '%s')" % (book_url, is_book_stored[0]))
            conn.commit()
        except Exception as e:
            print(book_name,' 保存失败：',e)
            conn.rollback()
            os.exit(0)
