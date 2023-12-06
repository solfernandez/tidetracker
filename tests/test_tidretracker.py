import os
from datetime import datetime
from main import datapoints_from_table, Datapoint

# THIS_DIR = os.path.dirname(os.path.realpath(__file__))
# html = THIS_DIR + '/tabla.html'


datapoints_list = set([
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='Mar del Plata', height=1.22),
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='Santa Teresita', height=1.4),
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='San Clemente (*)', height=None),
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='Oyarvide (*)', height=0.67),
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='Atalaya (**)', height=0.69),
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='La Plata', height=1.13),
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='Pilote Norden (***)', height=0.82),
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='Buenos  Aires', height=1.15),
    Datapoint(date_time=datetime(2023, 12, 4, 15, 45), location='San Fernando', height=1.5)])


def test_datapoints_from_table():
    with open('/home/sol/codigo/tidetracker/tabla.html') as f:
        html = f.read()
    datapoints = datapoints_from_table(html)
    assert datapoints == datapoints_list
