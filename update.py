import requests

print('Beginning file download with requests')

url = 'https://projects.fivethirtyeight.com/nba-model/nba_elo_latest.csv'
r = requests.get(url)

with open('/Users/tylerharkcom/Desktop/nba/nba_elo_latest.csv', 'wb') as f:
    f.write(r.content)

# Retrieve HTTP meta-data
print(r.status_code)
print(r.headers['content-type'])
print(r.encoding)
