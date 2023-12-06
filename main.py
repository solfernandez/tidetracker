from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Datapoint:
    datetime: datetime
    location: str
    height: float


# read html

with open('tabla.html') as f:
    html = f.read()

# parse html and extract table
soup = BeautifulSoup(html, features = 'html.parser')
table = soup.find_all("table")[0]

# extract table rows

rows = BeautifulSoup(str(table), features = 'html.parser').find_all("tr")

'''
tablesoup = BeautifulSoup(str(table), features = 'html.parser')
# Extraer todas las filas
rows = []
for elem in tablesoup.find_all("tr"):
    rows.append(elem)
'''

# extract date and time of last measurement from first row

date, time = BeautifulSoup(str(rows[0]), 'html.parser').find_all("th")[2].text.strip().split()
print( 'datetime:', date, time)

'''
# Extraer elementos de la primera fila
horarios = []
for el in BeautifulSoup(str(rows[0]), 'html.parser').find_all("th"):
    horarios.append(el)

# guardar datos de ultima medicion
fecha, hora = horarios[2].text.strip().split()
print('datetime:', fecha, hora)
'''



locations = []
heights = []
for row in rows[1:]:
    els = BeautifulSoup(str(row), 'html.parser').find_all("td")
    locations.append(els[1].text.strip())
    heights.append(els[2].text.strip())
print('locations:', locations)
print('heights:', heights)



# Locations
#locations = []
#for element in tablesoup.find_all("span"):
#    locations.append(element.string)
#print(locations)



