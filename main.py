from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import datetime
import sqlite3
import requests
import time

@dataclass(eq=True, frozen=True)
class Datapoint:
    date_time: datetime
    location: str
    height: float

def datapoints_from_table(html: str) -> set[Datapoint]:
    # parse html and extract table
    soup = BeautifulSoup(html, features='html.parser')
    table = soup.find_all("table")[0]

    # extract table rows
    rows = BeautifulSoup(str(table), features='html.parser').find_all("tr")

    # extract date and time of last measurement from first row
    date, time = BeautifulSoup(str(rows[0]), 'html.parser').find_all("th")[2].text.strip().split()
    date_time = datetime.strptime(date + ' ' + time, '%d/%m/%Y %H:%M')

    # extract location and tide height from following rows, create datapoints

    datapoints = set()
    for row in rows[1:]:
        els = BeautifulSoup(str(row), 'html.parser').find_all("td")
        location = els[1].text.strip()
        for char in ['(', ')', '*', '\n']:
            location = location.replace(char, '')
        location = location.strip()
        height_str = els[2].text.strip().replace(',', '.')
        try:
            height = float(height_str)
        except ValueError:
            height = None
        datapoints.add(Datapoint(date_time=date_time, location=location, height=height))
    return datapoints


def create_db_and_table_tides(db: str) -> str: # puede devolver el conector?
    # connect to db (create it if it does not exist)
    with sqlite3.connect(db) as con:
        cursor = con.cursor()
        # create table 'tides' if it does not exist:
        res = cursor.execute('SELECT count(*) FROM sqlite_master WHERE type="table" AND name="tides";')
        if res.fetchall()[0][0] == 0:
            cursor.execute('CREATE TABLE tides (date_time TEXT, location TEXT, height REAL);')
        return db

def add_datapoints_to_db(db: str, datapoints: set) -> None:
    with sqlite3.connect(db) as con:
        cursor = con.cursor()

    for datapoint in datapoints:
        date_time = datapoint.date_time.strftime('%Y-%m-%d %H:%M:%S')
        location = datapoint.location
        height = datapoint.height
        params = (date_time, location, height)
        # check if record exists, if not, add it to db
        if not cursor.execute(
                f'SELECT * from tides WHERE date_time = "{date_time}" AND location = "{location}"').fetchone():
            cursor.execute('INSERT INTO tides VALUES (?, ?, ?)', params)
            con.commit()


def collect_current_tide_data(url:str) -> None:
    # collect last hour data

    r = requests.get(url, auth=('user', 'pass'))
    html = r.text

    # extract datapoints from html table

    datapoints = datapoints_from_table(html)

    # create db and table "tides"
    db = create_db_and_table_tides('weather.db')

    # insert datapoints in db
    add_datapoints_to_db(db, datapoints)

    #con.close()


if __name__ == '__main__':

    url = 'http://www.hidro.gov.ar/oceanografia/alturashorarias.asp'
    while True:
        collect_current_tide_data(url)
        time.sleep(3600)


# TODO: make function to convert query results to datapoints

''' 
with sqlite3.connect('weather.db') as con:
    cur = con.cursor()
    res = cur.execute('SELECT * FROM tides')
    results = res.fetchall()
    for result in results:
        print(result)
'''