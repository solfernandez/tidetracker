import os
from datetime import datetime
import sqlite3
from main import datapoints_from_table, add_datapoints_to_db, Datapoint, create_db_and_table_tides



datapoints_set = set([
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='Mar del Plata', height=1.22),
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='Santa Teresita', height=1.4),
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='San Clemente', height=None),
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='Oyarvide', height=0.67),
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='Atalaya', height=0.69),
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='La Plata', height=1.13),
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='Pilote Norden', height=0.82),
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='Buenos  Aires', height=1.15),
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='San Fernando', height=1.5)])


def test_datapoints_from_table():
    THIS_DIR = os.path.dirname(os.path.realpath(__file__))
    html = THIS_DIR + '/tabla.html'
    print(html)
    with open(html) as f:
        html = f.read()
    datapoints = datapoints_from_table(html)
    assert datapoints == datapoints_set


def test_add_datapoints_to_db(tmp_path):
    db = create_db_and_table_tides(str(tmp_path) + '/test_db.db')
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        res = cur.execute('SELECT * FROM tides')
        results = res.fetchall()
        for result in results:
            date_time = result[0]
            location = result[1]
            height = result[2]
            datapoint = Datapoint(date_time=datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S'), location=location, height=height)
            assert datapoint in datapoints_set

