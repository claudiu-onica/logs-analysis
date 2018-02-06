#!/usr/bin/env python3
"""logs-analysis produces reports based on the data from
the database 'news'.
"""

import psycopg2

# Define a static variable  the database name
DBNAME = 'news'


def fetch_data(select_str):
    """fetch_data function connects the the database, executes
    the passed in query and returns the results.

    Arguments:
        select_str {string} -- psql query to be executed

    Returns:
        list -- list of tuples containig the results of the query
    """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(select_str)
    res = c.fetchall()
    db.close()
    return res


def create_view(view):
    """create_view - creates the views used to calculate the failed requests.

    Arguments:
        view {string} -- psql CREATE VIEW command

    Returns:
        Boolean -- True if the command succeeded othewise it returns False
    """
    ret = True
    db = None
    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        c.execute(view)
        db.commit()
    except psycopg2.Error as e:
        print(e)
        ret = False
    if db:
        db.close()
    return ret


def get_popular_articles():
    """get_popular_articles returns the most popular three articles of all time.

    Returns:
        string -- formated string containing the name and number of views
        of the top 3 most popular articles
    """
    query = """select a.title, count(l.path) as num from articles a, log l where l.path
            = concat('/article/', a.slug) group by a.title
            order by num desc limit 3"""
    res = fetch_data(query)
    articles = "\n".join("%s - %s views" % (article, num)
                         for article, num in res)
    return articles


def get_popular_authors():
    """get_popular_authors returns the most popular article authors of all time.

    Returns:
        string -- list of the most popular authors
    """
    query = """select au.name, count(l.path) as num from articles a, log l, authors au
            where a.author = au.id and l.path = concat('/article/', a.slug)
            group by au.name order by num desc"""
    res = fetch_data(query)
    authors = "\n".join("%s - %s views" % (author, num) for author, num in res)
    return authors


def get_most_errors():
    """get_most_errors returns the days on wich more than 1% of requests
    lead to errors.

    Returns:
        string -- formated string containing the date and the percentage
                    of failed requests.
    """
    errors_view = """create or replace view daily_errors as
                    select l.time::date as day, count(l.status) as error_count
                    from log l where l.status != '200 OK'
                    group by day order by day;"""
    requests_view = """create or replace view daily_requests as
                    select l.time::date as day, count(l.status) as requests
                    from log l group by day order by day;"""
    query = """ select to_char(r.day, 'FMMonth FMDD, YYYY') as day,
                to_char(e.error_count*100/r.requests::float, 'FM990D9999')
                as percent
                from daily_requests r, daily_errors e where r.day = e.day and
                e.error_count*100/r.requests::float > 1
                order by percent desc"""
    if create_view(errors_view) and create_view(requests_view):
        res = fetch_data(query)
        articles = "\n".join("%s - %s%% errors" % (article, num)
                             for article, num in res)
    return articles


def print_logs():
    """print_logs prints all three reports."""
    print("\nThe most popular three articles of all time:\n")
    print(get_popular_articles())
    print("\nThe most popular article authors of all time:\n")
    print(get_popular_authors())
    print("\nDays on wich more than 1% of requests lead to errors:\n")
    print(get_most_errors())


print_logs()
