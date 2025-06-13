# Straviz

Not a very functional, efficient or robust way of displaying strava data. Simply a project to learn Grafana, SQL, and improve my OOP in Python. The set up below should get you started but hopefully it will be automated in a script one day.

### Installation guide

- Clone this repo.
- Navigate to the source folder: `cd straviz/src`

### mysql
- Install mysql with apt - `sudo apt install mysql server`
- Open mysql with `sudo mysql`
- Make sports database: `CREATE DATABASE sports;`

- Set up an `api_user` user: `CREATE USER 'api_user'@'localhost' IDENTIFIED BY 'your_secure_password';` obviously replacing `your_secure_password`
- Save `your_secure_password` in a file `mysql_pw`
- Then give permission to the api_user: `GRANT ALL PRIVILEGES ON sports.* TO 'api_user'@'localhost'; FLUSH PRIVILEGES; EXIT;`

- Select sports db: `USE sports;`
- Create activities table: ``
```sh
CREATE TABLE activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(50),
    act_date DATE,
    moving_time INT,        -- in seconds
    distance FLOAT,         -- in meters (or km, depending on your data)
    avgHR INT,              -- average heart rate
    maxHR INT,              -- maximum heart rate
    stress INT              -- Training Stress Score (TSS)
)
```
- Create copy of activities table: same command as above replacing activities wth copy.
- Create fitness table: `create table fitness (id INT, date DATE, fitness FLOAT, fatigue FLOAT, form FLOAT);`


### strava API
- Follow this guide for setting up strava developer API: https://developers.strava.com/docs/getting-started/
    - A note on scope: - if you have `scope:read` you can access public activities only but can access private ones too if you have `scope:read_all`)
- Save client id and client secret in file client_data.txt
- Save access token, refresh token and expiry date in token.txt:
```sh
echo $YOUR_EXPIRE_TIME >> tokens.txt
echo $YOUR_ACCESS_TOKEN >> tokens.txt
echo $YOUR_REFRESH_TOKEN >> tokens.txt
```
    - Expire time can be found on the web and then using command line (e.g.): `date -d 2025-06-13T21:36:23Z +%s >> tokens.txt`

### setting up a python evironment
- Make python environment:
```py
python3 -m venv straviz_env
source straviz_env/bin/activate
pip install -r requirements.txt
```

### GET some activities
- Save epoch in a file `epoch` for 2 weeks ago, using: `date -d "2 weeks ago" +%s > epoch`
- Run `sync.sh`. 
- Run `python3 back_date.py` a few times to get some data into the table (this assumes you have an active strava account with a few months of sporting activities to draw from).
- Run `python3 adjust_copy.py`


### Grafana
- Install grafana with apt - follow steps on website...
- Start grafana server if necessary or if coming back: `sudo systemctl start grafana-server`
- Login to grafana admin and change admin password, save password
- Setup mysql backend: `Menu -> Connections -> Data sources -> Add new data source`. Search MySQL and fill in details about api_user. Host url should be: `localhost:3306` with database: `sports`.
- Load dashboard by `Menu -> Dashboards -> New -> Import` and when prompted upload the Activities.json file.
- Et voila!

## Usage

- Now you can come to this repo once a day/week/month, run `sync.sh` and fill in the gym sessions you did each day or add to the sports type folder to add even more activities (e.g. climbing sessions). Then watch your progress on grafana.
