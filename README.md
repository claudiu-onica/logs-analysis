# logs-analysis
Views created:

"create or replace view daily_errors as
    select l.time::date as day, count(l.status) as error_count
    from log l where l.status != '200 OK' group by day order by day"

"create or replace view daily_requests as
    select l.time::date as day, count(l.status) as requests
    from log l group by day order by day"
