

import psycopg2

DBNAME = 'news'


def get_posts():
    """Return all posts from the 'database', most recent first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select content, time from posts order by time desc")
    res = c.fetchall()
    db.close()
    return res


def add_post(content):
    """Add a post to the 'database' with the current timestamp."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("insert into posts values(%s)", (content,))
    db.commit()
    db.close()


def fetch_data(select_str):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(select_str)
    res = c.fetchall()
    db.close()
    return res


def get_popular_articles():
    query = """select a.title, count(l.path) as num from articles a, log l where l.path
            like format(\'%%%s%%\', a.slug) group by a.title
            order by num desc limit 3"""
    res = fetch_data(query)
    articles = "\n".join("%s - %s views" % (article, num) for article, num in res)
    return articles


def get_popular_authors():
    query = """select au.name, count(l.path) as num from articles a, log l, authors au
            where a.author = au.id and l.path like format('%%%s%%', a.slug)
            group by au.name order by num desc"""
    res = fetch_data(query)
    authors = "\n".join("%s - %s views" % (author, num) for author, num in res)
    return authors


def get_most_errors():
    daily_request_view = """create or replace view daily_errors as
    select l.time::date as day, count(l.status) as error_count
    from log l where l.status != '200 OK' group by day order by day"""

    daily_errors_view = """create or replace view daily_requests as
    select l.time::date as day, count(l.status) as requests
    from log l group by day order by day"""

    query = """ select to_char(r.day, 'Month DD, YYYY') as day,
    to_char(e.error_count*100/r.requests::float, 'FM990D9999') as percent
    from daily_requests r, daily_errors e where r.day = e.day and
    e.error_count*100/r.requests::float > 1 order by percent desc"""
    res = fetch_data(query)
    articles = "\n".join("%s - %s%% errors" % (article, num) for article, num in res)
    return articles


def print_logs():
    print("\nThe most popular three articles of all time:")
    print(get_popular_articles())
    print("\nThe most popular article authors of all time:")
    print(get_popular_authors())
    print("\nDays on wich more than 1% of requests lead to errors:")
    print(get_most_errors())


print_logs()
