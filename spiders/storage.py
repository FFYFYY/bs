

def stored_mysql(conn, cur, i, book_name, author, intro=None, img_url=None, category=None):
    try:
        cur.execute("select * from books where book_name='%s' limit 1" % book_name)
        result = cur.fetchone()
        print(result)
        if result is None:
            cur.execute(
                "insert into books(book_name, author, intro, img_url, type) values('%s', '%s', '%s', '%s', '%s')"
                % (book_name, author, intro, img_url, category))
            conn.commit()
            with open('message/errors.txt', 'w') as f:
                f.write(str(i + 1))
            print(i, book_name, "*************************", "保存成功")
        else:
            if None in result:
                cur.execute("")
                conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
