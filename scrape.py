from bs4 import BeautifulSoup, Comment
import requests
import pandas as pd

def tournStats():
    stats = []
    file = open('teams.txt', 'r')
    for row in file.read().split('\n'):
        team = str(row)
        team = team.lower()
        team = team.replace(' ', '-')
        team = team.replace('*', '')
        team = team.replace('.', '')
        print team
        stats.append([team, defence(team), sos(team)])
    return stats

def getStats(team):
    url = "https://www.sports-reference.com/cbb/schools/" + team + "/2018.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    per_game = soup.find('div', id='all_per_game_conf')
    comments = per_game.find(string=lambda text: isinstance(text, Comment))
    rows = BeautifulSoup(comments, 'lxml').findAll('tr')
    arr = []
    for row in rows[1:11]:
        rw = [team]
        cells = row.findAll("td")
        for i in [0,8,9,11,12,14,15]:
            rw.append(str(cells[i].text))
        arr.append(rw)
    return arr

def defence(team):
    url = "https://www.sports-reference.com/cbb/schools/" + team + "/2018.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    dr = soup.find('div', id='info')
    rate = dr.findAll('p')
    return rate[10].text.split()[1]

def sos(team):
    url = "https://www.sports-reference.com/cbb/schools/" + team + "/2018.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    dr = soup.find('div', id='info')
    rate = dr.findAll('p')
    return rate[8].text.split()[1]

print sos("new-mexico-state")
my_df = pd.DataFrame(tournStats())
print(my_df.head())
my_df.to_csv('ratings.csv', index=False, header=False)

