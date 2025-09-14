# Straviz

Not a very functional, efficient or robust way of displaying Strava data. Simply a project to learn Grafana, SQL, and improve my OOP in Python. The set up below should get you started but hopefully it will be automated in a script one day.

Disclaimer: This mini-app is in no way affiliated with Strava.

### Installation guide

- Clone this repo.
- Navigate to the source folder: `cd straviz/src`

### MySQL

Using MySQL (or another server-based SQL framework) is essential for displaying data in Grafana as it does not yet take a memory-based database option like SQLite.

- Install mysql with apt - `sudo apt install mysql server`
    - Then open MySQL with `sudo mysql`
- Make a database and set up an 'api_user' user with all privileges on that database. Save YOUR_PASSWORD and the name of the database, user and host in the `.env` credentials file. 
```
CREATE DATABASE sport;
USE sport;
CREATE USER 'api_user'@'localhost' IDENTIFIED BY 'YOUR_PASSWORD';
GRANT ALL PRIVILEGES ON sport.* TO 'api_user'@'localhost'; FLUSH PRIVILEGES; EXIT;
```
- Now create the activities table to store the Strava activities in.
```sh
CREATE TABLE activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sid INT,                -- strava ID
    type VARCHAR(50),       -- type of activity
    date DATE,              -- date of activity
    moving_time INT,        -- in seconds
    distance FLOAT,         -- in metres
    elevation FLOAT,        -- in metres
    avg_speed FLOAT,        -- in metres/second
    avgHR INT,              -- average heart rate
    maxHR INT,              -- maximum heart rate
    stress INT              -- Training Stress Score (TSS)
)
```
- Now create a daily fitness table with total stress for each day and subsequent fitness, fatigue and form values: 
```
CREATE TABLE fitness (
    date DATE PRIMARY KEY,              -- date of each day since first activity on Strava
    stress FLOAT NOT NULL DEFAULT 0,    -- total stress score for each day
    fitness FLOAT NOT NULL,             -- fitness value each day
    fatigue FLOAT NOT NULL,             -- fatigue value each day
    form FLOAT NOT NULL                 -- form value each day
);
```


### Strava API
- Follow this guide for setting up strava developer API: https://developers.strava.com/docs/getting-started/
    - Make sure that when you get to the stage of entering in the URL `http://www.strava.com/oauth/authorize?client_id=[REPLACE_WITH_YOUR_CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read` that you add `,activity:read_all` to the end otherwise you won't be able to read activities.
    - A note on scope: - if you have `scope=read,activity:read` you can access public activities only but can access private ones too if you have `scope=read,activity:read_all`)
- Save client id, client secret, access and refresh tokens, expiry time (as epoch), and MySQL user details in a `src/config/.env` file. An example template is given below and in the `src/config` folder.
```sh
CLIENT_ID=
CLIENT_SECRET=
EXPIRES_AT=
ACCESS_TOKEN=
REFRESH_TOKEN=
MYSQL_PW=
MYSQL_USER="api_user"
MYSQL_HOST="localhost"
MYSQL_DATABASE="sport"
LAST_SYNC=
```
- Save the LAST_SYNC key to 2 weeks ago (or further back if you want), using: `date -d "2 weeks ago" +%s`
### Setting up a python evironment
- Make python environment:
```py
python3 -m venv straviz_env
source straviz_env/bin/activate
pip install -r requirements.txt
```

### GET some activities
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
