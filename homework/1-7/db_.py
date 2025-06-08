import base64
import psycopg2
from config import DB_CONFIG

# --- part of articles ---

def get_articles(article_id=-1, user_id=-1, page=1, pre_page=10, limited=-1, preview=False):
    """
    返回一个列表，
    如果没有给限制那么所有数据都在一个列表里，
    如果有限制这个列表里会包含多个列表
    :param preview:
    :param article_id:
    :param pre_page: 每页行数，默认10个条目
    :param page: 当前页数，默认第一页
    :param user_id: 用户id
    :param limited: 单页限制
    :return:
    """
    r = []
    offset = (page - 1) * pre_page
    with psycopg2.connect(DB_CONFIG()) as db:
        with db.cursor() as cur:
            if article_id > 0:
                sql = "select * from articles where article_id=%s"
                cur.execute(sql, (article_id, ))
            else:
                if user_id > 0:
                    sql = "select * from articles where id=%s order by created_timestamp desc"
                    params = [user_id]
                else:
                    sql = "select * from articles order by created_timestamp desc"
                    params = []
                if limited > 0:
                    sql = f"{sql} limit %s offset %s"
                    cur.execute(sql, params + [limited, offset])
                else:
                    cur.execute(sql, params)
            results = cur.fetchall()
    for i in results:
        if preview and len(i[3]) > 300:
            this = {
                "article_id": i[0],
                "user_id": i[1],
                "title": i[2],
                "content": i[3][:300]+"......MORE>>>",
                "created_timestamp": i[4],
                "updated_timestamp": i[5]
            }
        else:
            this = {
                "article_id": i[0],
                "user_id": i[1],
                "title": i[2],
                "content": i[3],
                "created_timestamp": i[4],
                "updated_timestamp": i[5]
            }
        r.append(this)
    return r


def article_update(article_id, title, content):
    # title_b64 = base64.b64encode(title.encode("utf-8")).decode("ascii")
    # content_b64 = base64.b64encode(content.encode("utf-8")).decode("ascii")
    sql = "update articles set title=%s, content=%s where article_id=%s"

    with psycopg2.connect(DB_CONFIG()) as db:
        with db.cursor() as cur:
            # cur.execute(sql, (title_b64, content_b64, article_id))
            cur.execute(sql, (title, content, article_id))
            if cur.rowcount > 0:
                print("ok")
                return 0
            else:
                print("e")
                return -1

def article_insert(user_id, title, content):
    # title_b64 = base64.b64encode(title.encode("utf-8")).decode("ascii")
    # content_b64 = base64.b64encode(content.encode("utf-8")).decode("ascii")
    sql = "insert into articles (id, title, content) values (%s, %s, %s)"

    with psycopg2.connect(DB_CONFIG()) as db:
        with db.cursor() as cur:
            # cur.execute(sql, (user_id, title_b64, content_b64))
            cur.execute(sql, (user_id, title, content))
            if cur.rowcount > 0:
                print("ok")
                return 0
            else:
                print("e")
                return -1

def article_delete(article_id):
    sql = "delete from articles where article_id=%s"
    with psycopg2.connect(DB_CONFIG()) as db:
        with db.cursor() as cur:
            cur.execute(sql, (article_id, ))
            if cur.rowcount > 0:
                print("ok")
                return 0
            else:
                print("e")
                return -1

def article_search(keywords):
    sql = "select * from articles where title ilike %s order by created_timestamp desc"
    r = []
    with psycopg2.connect(DB_CONFIG()) as db:
        with db.cursor() as cur:
            cur.execute(sql, (f"%{keywords}%", ))
            results = cur.fetchall()
    for i in results:
        # default preview
        if len(i[3]) > 300:
            this = {
                "article_id": i[0],
                "user_id": i[1],
                "title": i[2],
                "content": i[3][:300] + "......MORE>>>",
                "created_timestamp": i[4],
                "updated_timestamp": i[5]
            }
        else:
            this = {
                "article_id": i[0],
                "user_id": i[1],
                "title": i[2],
                "content": i[3],
                "created_timestamp": i[4],
                "updated_timestamp": i[5]
            }
        r.append(this)
    return r

# --- end of articles ---

# --- part of users ---

def add_user(nickname, email, password):
    # no passwd encrypt, this is just a demo
    if len(password) < 8: return -1
    sql = "insert into users (nickname, email, passwd) values (%s, %s, %s)"
    with psycopg2.connect(DB_CONFIG()) as db:
        with db.cursor() as cur:
            cur.execute(sql, (nickname, email, password))
            if cur.rowcount > 0:
                return 0
    return 1

def get_user(email):
    sql = "select * from users where email=%s"
    with psycopg2.connect(DB_CONFIG()) as db:
        with db.cursor() as cur:
            cur.execute(sql, (email,))
            result = cur.fetchone()
    if result:
        return {"status": 0, "msg": "ok", "id": result[0], "nickname": result[1]}
    return {"status": 1, "msg": "user not found"}

# --- end of users ---

# --- part of auth ---

def auth(email, password):
    # no passwd encrypt, this is just a demo
    sql = "select * from users where email=%s"
    with psycopg2.connect(DB_CONFIG()) as db:
        with db.cursor() as cur:
            cur.execute(sql, (email, ))
            result = cur.fetchone()
    if not result:
        # print("user not found")
        return {"status": 1, "msg": "user not found"}
    if password == result[3]:
        return {"status": 0, "msg": result[1], "id": result[0]}
    # print("paasword incorrect")
    return {"status": 2, "msg": "paasword incorrect"}

# --- end of auth ---

def _article_random_insert(m:int):
    import random
    flag = False
    this = ""
    for i in range(5):
        this = "".join(random.sample('zyxwvutsrqponmlkjihgfedcba', 5))
        do = add_user(nickname=this, email=f"{this}@abc.com", password=f"{this}12345")
        if do == 0:
            flag = True
            break
        i+=1
    if not flag:
        return "cannot insert user in 5 times."
    user_id = get_user(f"{this}@abc.com")["id"]
    for i in range(m):
        title = "".join(random.sample('zyxwvutsrqponmlkjihgfedcba', 10))
        content = "".join(random.choices('zyxwvutsrqponmlkjihgfedcba', k=300))
        do = article_insert(user_id, title, content)
        if do == 0:
            print(f"ok: {title}")
    return "finish"

if __name__ == '__main__':
    # add_user("user123", "123123@eee.com", "qweqweasd")
    # print(auth("123123@eee.com", "qweqweasd"))
    # print(auth("123123@eee.com", "qweqweasd1"))
    # print(article_insert("3", "this is a test article 12312", "skjadhfukas3242342432111111jfdha"))
    # print(get_articles(limited=2))
    # print(_article_random_insert(5))
    print(get_articles(user_id=6))