import requests
from bs4 import BeautifulSoup

# page = requests.get('https://www.nasdaq.com/symbol/cvx/insider-trades')
page = requests.get('https://www.nasdaq.com/symbol/cvx/insider-trades?page=2')
soup = BeautifulSoup(page.text, 'html.parser')
table = soup.find('table', {'class':'certain-width'})
print(table)
data = []
rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele]) # Get rid of empty values
with open('page.html', 'w', encoding='utf-8') as file:
    file.write(str(data))
# Create a BeautifulSoup object
