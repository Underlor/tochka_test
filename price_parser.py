import requests
from bs4 import BeautifulSoup

page = requests.get('http://www.nasdaq.com/symbol/cvx/historical')
soup = BeautifulSoup(page.text, 'html.parser')
table = soup.find('table').parent.find_next_siblings()[3].find('tbody')
rows = table.find_all('tr')
data = []
for row in rows:
    cols = row.find_all('td')
    price = cols[4].text.strip()
    if price:
        data.append(price) # Get rid of empty values
with open('page.html', 'w') as file:
    file.write(str(data))
# Create a BeautifulSoup object
