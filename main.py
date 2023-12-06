from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import datetime


@dataclass(eq=True, frozen=True)
class Datapoint:
    date_time: datetime
    location: str
    height: float


# read html

with open('tabla.html') as f:
    html = f.read()


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
        location = els[1].text.strip().replace('\n', '')
        height_str = els[2].text.strip().replace(',', '.')
        try:
            height = float(height_str)
        except ValueError:
            height = None
        datapoints.add(Datapoint(date_time=date_time, location=location, height=height))
    return datapoints


datapoints = datapoints_from_table(html)
for datapoint in datapoints:
    print(datapoint)

