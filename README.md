# logs-analysis
===

## Description
logs-analysis is a reporting tool that uses information from 'news' database to answer the folowing questions:
1. What are the most popular three articles of all time? 
2. Who are the most popular article authors of all time? 
3. On which days did more than 1% of requests lead to errors?

## Requirements
* Python 3
* psycopg2;

    Psycopg is the most popular PostgreSQL database adapter for the Python programming language. Its main features are the complete implementation of the Python DB API 2.0 specification and the thread safety (several threads can share the same connection). It was designed for heavily multi-threaded applications that create and destroy lots of cursors and make a large number of concurrent INSERTs or UPDATEs. It can be installed using pip:

        `pip install psycopg2`
    

## Installation
* Fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm
* Clone the repository https://github.com/claudiu-onica/logs-analysis.git into the vagrant folder of your virtual machine
## Usage
In a terminal start the VM.

Navigate to "vagrant\LogsanalysisProject" then execute the following command: 
   
    `python logs-analysis.py`



The application uses the following views to calculate the percentage of the failed requests. The views are created by the application:

"create or replace view daily_errors as
    select l.time::date as day, count(l.status) as error_count
    from log l where l.status != '200 OK' group by day order by day"

"create or replace view daily_requests as
    select l.time::date as day, count(l.status) as requests
    from log l group by day order by day"
    
## Result
![Program output example](https://github.com/claudiu-onica/logs-analysis/blob/master/log_result.png)
