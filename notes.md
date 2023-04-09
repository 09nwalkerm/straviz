# STRAVA/API/DATABASE

- Jotting down some notes and thoughts to save between programming sessions

## 26.03.2023

### The python mysql.connector mod

- https://www.tutorialspoint.com/python_data_access/python_mysql_insert_data.htm#

- https://www.w3schools.com/python/python_mysql_getstarted.asp

### MySQL

- Have created user api_user@localhost with insert and select privialges for the sport database
	- Password is saved in key pass.

- Created the sport database with the activities table
	- Which contains the values date, time, type, distance
	- Should be enough to get on with for now.

- Start Mysql server: `systemctl start mysql`

- Check status: `systemctl status mysql`

- Stop server: `systemctl stop mysql`

- May need to figure out the diff between mysql and mysqld_safe

- Base installation directory for MySQL is /usr/

- `mysql -u root -p` to connect to the mysql server.

- For help: https://dev.mysql.com/doc/mysql-getting-started/en/

```sh
    #mycursor = mydb.cursor()
    #cursor.execute("SELECT * FROM table ORDER BY id DESC LIMIT 1")
    #result = cursor.fetchone()
```

```sh
import sys

print(f"please give a number")
text = int(input())

print(f"your number is {text :d}")
```

- https://www.cyberciti.biz/tips/linux-unix-get-yesterdays-tomorrows-date.html

- `echo 1679319002 > epoch`

- `SHOW GLOBAL VARIABLES LIKE 'PORT';`

- Mysql: port 3306
- grafana: port 3000

- `select * from mysql.user;` to see users and permissions for database.

- `SELECT date,distance from sport.activities`

- `sudo grafana server`

- The null value problem: https://learn.microsoft.com/en-us/azure/azure-sql-edge/imputing-missing-values

- `GRANT CREATE ON sport.activities TO 'api_user'@'localhost';`

- `mysql> select * from activities where date > '2023-03-20';`

```sh
date = datetime.datetime(2003,8,1,12,4,5)
for i in range(5): 
    date += datetime.timedelta(days=1)
    print(date) 
```

- `mysql> select * from copy where date > '2023-03-20' AND type="Run";`

- `select date,SUM(moving_time) over (order by date) as total from copy;`

- Rolling average: https://chartio.com/learn/postgresql/how-to-create-a-rolling-period-running-total/

- `select date,distance,DATE_ADD(date, INTERVAL -3 DAY) as date_back, SUM(distance) OVER (BETWEEN date_back AND date) from copy where type="Run";`

- https://stackoverflow.com/questions/19213633/create-a-rolling-sum-over-a-period-of-time-in-mysql

- 

MySQL 8 has window functions that are meant for this exact case:

SELECT
    SUM(time_spent) OVER(
         ORDER BY date RANGE BETWEEN INTERVAL 7 DAY PRECEDING 
         AND CURRENT ROW) AS total,
    date
FROM rolling_total

ORDER BY date determines the dimension you are using for the rolling window.

RANGE BETWEEN A AND B defines the filter criteria of the window.

INTERVAL 7 DAY PRECEDING means all 7 days prior to the current row.

CURRENT ROW uses the value of the current row.

- `SELECT SUM(distance) OVER (ORDER BY date RANGE BETWEEN INTERVAL 7 DAY PRECEDING AND CURRENT ROW) AS rolling_7_day, date FROM copy WHERE type="Run";`

- `select yearweek(date) as time, sum(moving_time) as total from copy group by time;`

- `with data as (select date,distance,moving_time from copy where type="Run") select convert(date_format(date,'%x %v'),char) as times, sum(distance) as total from data group by times;`








