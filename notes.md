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