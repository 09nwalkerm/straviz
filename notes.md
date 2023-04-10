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

- `sudo cp /var/lib/grafana/grafana.db ./dashboard/`

- `mysql> select date,DATE_FORMAT(ADDDATE(date, INTERVAL 2-DAYOFWEEK(date) DAY), '%Y-%m-%d') as week, moving_time from copy order by date;`

- `with data as (select date,distance,moving_time from copy where type="Run") select DATE_FORMAT(ADDDATE(date, INTERVAL 2-DAYOFWEEK(date) DAY), '%Y-%m-%d') as weeks, sum(moving_time) as total from data group by weeks;`

```sh
>>> acts.json()
[{'resource_state': 2, 'athlete': {'id': 2495353, 'resource_state': 1}, 'name': 'A perfect Saturday ', 'distance': 25794.0, 'moving_time': 9075, 'elapsed_time': 10333, 'total_elevation_gain': 549.3, 'type': 'Run', 'sport_type': 'Run', 'workout_type': 0, 'id': 8855402137, 'start_date': '2023-04-08T09:13:39Z', 'start_date_local': '2023-04-08T10:13:39Z', 'timezone': '(GMT+00:00) Europe/London', 'utc_offset': 3600.0, 'location_city': None, 'location_state': None, 'location_country': 'United Kingdom', 'achievement_count': 1, 'kudos_count': 27, 'comment_count': 0, 'athlete_count': 2, 'photo_count': 0, 'map': {'id': 'a8855402137', 'summary_polyline': 'igwyHt|cYcBOg@DoAnBuAlAmCzA{@MsDoBuHtA}IAkAUoCp@cAl@gBPqCfAi@p@aA\\gH|@k@`A_Bx@_LxBu@G}AbBkG`BsCZa@f@eAIyBy@yACwAk@_A_AkIyEsGaH_IgBwAbDS`CH~SU~Aa@`BlAnHWzG]bAuLvGa`@nZgF|CkSzNuLlJeBFm@tEaA`DMuAm@kAIq@y@y@eAkDk@yE{@gDQuAq@yAUuB_AsBOcAe@o@IeDu@cH_AsCC_AYcAi@DeAq@gAGa@k@CyEcAqK\\qBr@wBCoCLo@GmBRsBhA{Aj@kD`AoDpEiDcAqACqBUiA[wCMQy@@OLIn@SMUcGcByG{CwE_HwHmJgIuAH_D_CyC}EoDwI{FsJuDkEqDwC}JgL_JwM}@gCc@eCoEgc@}B_MaBoEwBgEsK}PuFmFuJ{HsHeFeCoAuFcBoJgBkPuBaDy@yC@_F{EGo@x@qChAmG|FsMZa@jAAfB_C~BaAp@{@lAf@N~@dBnB\\jBv@`@l@a@|AJvAzA|BX`AvAZlAAc@~Bc@d@nAr@TxBIfE`DzDr@|B`A|@`A\\ATi@b@QzBTbGxDvCpGz@Zv@g@vCMpAp@|BzBhAhEzDlEpBbDtAfGv@lCrGrLl@nCP`CtAlFf@rDr@n@pBR`CpB~@mB`Ak@tDiE|@a@h@ZfAIh@{Aa@YaAoCGaB}@yBGq@J_Bw@wCGaAcAgA_BeDqAqF@e@^s@JcAB}HZgDVaAXkInE]pDoBzA?~@vA|ArEz@hAnAd@~CHxAxAxAeAz@eDjBmCp@aC@jBNzACnFN|H`AfFJOAN`@N`AbBNlHx@d@bB|BdBp@j@vAfCdLbBfDBbB|@|@dB~F|@vBpBnCnI`JrFxDfD`EzBhDr@dB|ClJ`AfE`A|An@|Cd@IrAr@fAINtAIpCOz@r@dA|@jCpAUfB|AxANNe@NqEv@eCf@m@k@v@?l@XdAp@n@nEVpBi@|BFjBf@hArE^z@jAt@fAtAz@b@fDjGrBfBbCtFHpB`@l@p@~B`BlBv@fAt@~An@d@|BjCh@~@dBtDf@`Cf@dAFxAzAzGRxBtDzA`D^R\\AiBbAqDbAy@~@mA~B{@dHUvA}@jAL~@h@|Ai@vFm@xFiBhDc@bDkA~A_BlD{@nCj@jAlAvADrBhAtEdAfD~AlAbBvCrAxAhCt@~BvA\\t@t@UHPMfC\\hBt@', 'resource_state': 2}, 'trainer': False, 'commute': False, 'manual': False, 'private': False, 'visibility': 'everyone', 'flagged': False, 'gear_id': 'g4131227', 'start_latlng': [51.57, -4.29], 'end_latlng': [51.57, -4.29], 'average_speed': 2.842, 'max_speed': 5.8, 'average_cadence': 81.5, 'has_heartrate': True, 'average_heartrate': 153.6, 'max_heartrate': 178.0, 'heartrate_opt_out': False, 'display_hide_heartrate_option': True, 'elev_high': 191.5, 'elev_low': 0.7, 'upload_id': 9501951628, 'upload_id_str': '9501951628', 'external_id': '64319ed164c7f8145b59bc56.fit', 'from_accepted_tag': False, 'pr_count': 0, 'total_photo_count': 4, 'has_kudoed': False, 'suffer_score': 199.0}]
>>> 
```

- `echo 1676319002 > epoch`

```sh
with data as (select date,distance,moving_time from copy where type="Run" order by date) 
select DATE_FORMAT(ADDDATE(date, INTERVAL 2-WEEKDAY(date) DAY), '%Y-%m-%d') as weeks, 
sum(distance) as total from data where date > date_format(ADDDATE(current_date, INTERVAL -300 DAY),"%Y-%m-%d") group by weeks order by weeks;
```