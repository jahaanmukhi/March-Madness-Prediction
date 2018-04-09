import pandas as pd


data = pd.read_csv("stats.csv", header = None, names=["Team"
            , "Player", "2PA", "2PP", "3PA", "3PP", "FTA", "FTP"])

rtg = pd.read_csv("ratings.csv", header = None, names=["Team"
            , "DFRG", "SOS"])

data = data.fillna(0)



def bracket():
    teams = []
    file = open('teams.txt', 'r')
    for row in file.read().split('\n'):
        team = str(row)
        team = team.lower()
        team = team.replace(' ', '-')
        team = team.replace('*', '')
        team = team.replace('.', '')
        teams.append(team)
    return teams

def matchup(tA, tB):
    A = data.loc[data['Team'] == tA]
    B = data.loc[data['Team'] == tB]
    rateA = rtg.loc[rtg['Team'] == tA]
    rateB = rtg.loc[rtg['Team'] == tB]
    Afac =  rateA['DFRG'].values[0]
    Bfac = rateB['DFRG'].values[0]
    Asos = rateA['SOS'].values[0] + 10
    Bsos = rateB['SOS'].values[0] + 10
    diff = (abs(Asos-Bsos)/10.0)*2.0
    disA = False
    disB = False
    if Asos < Bsos:
        disA = True
    else:
        disB = True
    diffA = ((100 - Afac)*abs(100 - Afac))/300.0
    diffB = ((100 - Bfac)*abs(100 - Bfac))/300.0
    Afac = 1.0 - diffA
    Bfac = 1.0 - diffB
    scoreA = 0
    scoreB = 0
    maxA = maxB = 0
    pA = pB = ""
    for index, row in A.iterrows():
        player = row["Player"]
        score = 0
        score += shoot(row["2PA"], row["2PP"], Bfac, 2, diff, disA)
        score += shoot(row["FTA"], row["FTP"], 1.0, 2, 0, False)
        score += shoot(row["3PA"], row["3PP"], Bfac, 3, diff, disA)
        scoreA += score
        if score >= maxA:
            maxA = score
            pA = player

    for index, row in B.iterrows():
        player = row["Player"]
        score = 0
        score += shoot(row["2PA"], row["2PP"], Afac, 2, diff, disB)
        score += shoot(row["FTA"], row["FTP"], 1.0, 2, 0, False)
        score += shoot(row["3PA"], row["3PP"], Afac, 3, diff, disB)
        scoreB += score
        if score >= maxB:
            maxB = score
            pB = player

    print("{} : {} {} : {}".format(tA, scoreA, tB, scoreB))
    print("{} : {} {} : {}".format(pA, maxA, pB, maxB))
    if scoreA > scoreB:
        return tA
    else:
        return tB

import random

def shoot(a, p, d, v, diff, dis):
    score = 0
    if (dis):
        a -= diff
    shots = int(a)
    frac = a - shots
    if random.random() <= frac:
        shots += 1
    p = p*d
    for i in range(shots):
        bucket = random.random()
        if bucket < p:
            score += v
    return score

def generate(tA, tB, runs):
    winsA = 0
    winsB = 0
    for i in range(runs):
        if matchup(tA, tB) == tA:
            winsA += 1
        else:
            winsB += 1
    print("{} : {}, {} : {}".format(tA, winsA, tB, winsB))
    if winsA > winsB:
        return tA
    else:
        return tB

matchup("villanova", "cincinnati")
teams = []
while(len(teams) > 1):
    for x, y in zip(*[iter(teams)]*2):
        win = generate(x, y, 100)
        if win == x:
            teams.remove(y)
        else:
            teams.remove(x)
    print ("final {}".format(len(teams)))
    print "_____"
for x, y in zip(*[iter(teams)]*2):
    print (x, y)

