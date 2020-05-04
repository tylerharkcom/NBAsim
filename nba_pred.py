import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn
from scipy.stats import poisson,skellam

nba_1920 = pd.read_csv("https://projects.fivethirtyeight.com/nba-model/nba_elo_latest.csv")
# team1 = home
# team2 = away
nba_1920 = nba_1920[['team1','team2','score1','score2']]
nba_1920 = nba_1920.rename(columns={'team1': 'home', 'team2': 'away', 'score1': 'home_score', 'score2': 'away_score'})

print(nba_1920)
# nba_1920.head()
# nba_1920 = nba_1920[:-10]
# nba_1920.mean()
