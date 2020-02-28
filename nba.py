# Tyler Harkcom, 2020

# Simple CSV file reader that takes nba_elo.csv files from FiveThirtyEight (https://github.com/fivethirtyeight/data/tree/master/nba-forecasts)
# and produces a game-by-game summary of a user-inputted year's NBA results, given
# a year between 1946 and 2020. Standings are tabulated and saved in a dictionary.

# Things to add:
# 1. Support for playoffs -- round-by-round breakdowns, announcing series winners, etc.
# 2. Sorting of standings by wins -- being able to determine playoff seeding based on end-of-year record
# 3. Game prediction/simulation using elo_predictions on csv file -- randomly simulate (the rest of) the season using 538's predictions
# 4. Make things object-oriented and more modular for ease of translation between files

import csv
import random

current_year = 2020

east_atlantic = {"TOR", "BOS", "PHI", "BRK", "NYK"}
east_central = {"MIL", "IND", "CHI", "DET", "CLE"}
east_southeast = {"MIA", "ORL", "WAS", "CHO", "ATL"}
west_northwest = {"DEN", "OKC", "UTA", "POR", "MIN"}
west_pacific = {"LAL", "LAC", "SAC", "PHO", "GSW"}
west_southwest = {"HOU", "DAL", "MEM", "NOP", "SAS"}

east1 = {"TOR", "BOS", "PHI", "BRK", "NYK", "MIL", "IND", "CHI", "DET", "CLE", "MIA", "ORL", "WAS", "CHO", "ATL"}
west1 = {"DEN", "OKC", "UTA", "POR", "MIN", "LAL", "LAC", "SAC", "PHO", "GSW", "HOU", "DAL", "MEM", "NOP", "SAS"}

east = {"atlantic":{"TOR":{"wins":0, "losses":0}, "BOS":{"wins":0, "losses":0}, "PHI":{"wins":0, "losses":0}, "BRK":{"wins":0, "losses":0}, "NYK":{"wins":0, "losses":0}},
         "central":{"MIL":{"wins":0, "losses":0}, "IND":{"wins":0, "losses":0}, "CHI":{"wins":0, "losses":0}, "DET":{"wins":0, "losses":0}, "CLE":{"wins":0, "losses":0}},
         "southeast":{"MIA":{"wins":0, "losses":0}, "ORL":{"wins":0, "losses":0}, "WAS":{"wins":0, "losses":0}, "CHO":{"wins":0, "losses":0}, "ATL":{"wins":0, "losses":0}}}

# Key for nba_elo.csv column id's
# row[4] = team1
# row[5] = team2
# row[6] = team1_elo_pre
# row[7] = team2_elo_pre
# row[10] = team1_elo_post
# row[11] = team2_elo_post
# row[22] = team1_score
# row[23] = team2_score

def getCurrentResults(yr):
    with open('nba_elo.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        # target_year = int(input("Get NBA results for which year?"))
        target_year = yr
        results = {}
        # print("target_year = ")
        # print(target_year)
        if (target_year > 2020 or target_year < 1947):
            print("Error: Please insert a year between 1947 and 2020.")
        else:
            for row in csv_reader:
                if line_count == 0:
                    # print(f'Column names are {", ".join(row)}')
                    line_count += 1
                elif int(row[1]) != target_year:
                    line_count += 1
                else:
                    team1 = row[4]
                    if team1 not in results:
                        results[team1] = {"wins": 0, "losses": 0}
                        # print("Added " + team1 + " to results dict.")
                    team2 = row[5]
                    if team2 not in results:
                        results[team2] = {"wins": 0, "losses": 0}
                        # print("Added " + team2 + " to results dict.")
                    team1_score = row[22]
                    team2_score = row[23]
                    if team1_score == '': # Game hasn't been played yet
                        line_count += 1
                    elif int(team1_score) > int(team2_score):
                        print(f'{team1} beat {team2} by a score of {team1_score} - {team2_score}.')
                        if (row[3] == ''):
                            results[team1]['wins'] += 1
                            results[team2]['losses'] += 1
                            print(f'{team1} has a record of ' + str(results[team1]['wins']) + '-' + str(results[team1]['losses']))
                            print(f'{team2} has a record of ' + str(results[team2]['wins']) + '-' + str(results[team2]['losses']))
                    elif int(team2_score) > int(team1_score):
                        print(f'{team2} beat {team1} by a score of {team2_score} - {team1_score}.')
                        if (row[3] == ''):
                            results[team1]['losses'] += 1
                            results[team2]['wins'] += 1
                            print(f'{team1} has a record of ' + str(results[team1]['wins']) + '-' + str(results[team1]['losses']))
                            print(f'{team2} has a record of ' + str(results[team2]['wins']) + '-' + str(results[team2]['losses']))
                    else:
                        line_count += 1
        print(f'Processed {line_count} lines.')
        sortRankings(results)

def predictResults(yr):
    with open('nba_elo.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        # target_year = int(input("Get NBA results for which year: "))
        target_year = yr
        results = {}
        # print("target_year = ")
        # print(target_year)
        if (target_year > 2020 or target_year < 1947):
            print("Error: Please insert a year between 1947 and 2020.")
        else:
            for row in csv_reader:
                if line_count == 0:
                    # print(f'Column names are {", ".join(row)}')
                    line_count += 1
                elif int(row[1]) != target_year:
                    line_count += 1
                else:
                    team1 = row[4]
                    if team1 not in results:
                        results[team1] = {"wins": 0, "losses": 0}
                        # print("Added " + team1 + " to results dict.")
                    team2 = row[5]
                    if team2 not in results:
                        results[team2] = {"wins": 0, "losses": 0}
                        # print("Added " + team2 + " to results dict.")
                    team1_score = row[22]
                    team2_score = row[23]
                    if team1_score == '': # Game hasn't been played yet
                        team1prob = float(row[8])
                        predictGame(team1, team2, team1prob, results)
                    elif int(team1_score) > int(team2_score):
                        # print(f'{team1} beat {team2} by a score of {team1_score} - {team2_score}.')
                        if (row[3] == ''): # If it's still the regular season
                            results[team1]['wins'] += 1
                            results[team2]['losses'] += 1
                            # print(f'{team1} has a record of ' + str(results[team1]['wins']) + '-' + str(results[team1]['losses']))
                            # print(f'{team2} has a record of ' + str(results[team2]['wins']) + '-' + str(results[team2]['losses']))
                    elif int(team2_score) > int(team1_score):
                        # print(f'{team2} beat {team1} by a score of {team2_score} - {team1_score}.')
                        if (row[3] == ''): # If it's still the regular season
                            results[team1]['losses'] += 1
                            results[team2]['wins'] += 1
                            # print(f'{team1} has a record of ' + str(results[team1]['wins']) + '-' + str(results[team1]['losses']))
                            # print(f'{team2} has a record of ' + str(results[team2]['wins']) + '-' + str(results[team2]['losses']))
                    else:
                        line_count += 1

        print(f'Processed {line_count} lines.')
        sortRankings(results)

# def predictConfResults(yr):
#     with open('nba_elo.csv') as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         line_count = 0
#         if (target_year > 2020 or target_year < 1947):
#             print("Error: Please insert a year between 1947 and 2020.")
#         else:
#             for row in csv_reader:
#                 if line_count == 0 or int(row[1]) != target_year:
#                     line_count += 1
#                 else:
#                     team1 = row[4]
#                     team2 = row[5]
#                     team1_score = row[22]
#                     team2_score = row[23]
#                     if team1_score == '': # Game hasn't been played yet
#                         prob = float(row[8]) # Probability that Team1 wins, from FiveThirtyEight
#                         predictGame(team1, team2, prob)
#                     elif int(team1_score) > int(team2_score):
#                         if (row[3] == ''): # If it's still the regular season
#                             results[team1]['wins'] += 1
#                             results[team2]['losses'] += 1
#                     elif int(team2_score) > int(team1_score):
#                         if (row[3] == ''): # If it's still the regular season
#                             results[team1]['losses'] += 1
#                             results[team2]['wins'] += 1
#                     else:
#                         line_count += 1

def predictGame(team1, team2, prob, results):
    res = random.uniform(0.0, 1.0)
    if prob >= res: # Team1 wins
        results[team1]['wins'] += 1
        results[team2]['losses'] += 1
    else: # Team2 wins
        results[team1]['losses'] += 1
        results[team2]['wins'] += 1

def sortRankings(rankings):
    result = sorted(rankings.items(), key = lambda x: x[1]['wins'], reverse=True)
    print(result)


def startProg():
    print("Welcome to [Untitled NBA Predictor]. Please select a program to continue: ")
    print("1: NBA Historical Records, 2: Current NBA Season Simulator, 3: Single Team Simulation")
    inpt = int(input())
    if inpt == 1:
        print("Welcome to the NBA Historical Records Archive")
        print("Please enter a year from 1947 to 2019 to view historical data.")
        year = int(input())
        getCurrentResults(year)
    elif inpt == 2:
        print(f"Predicting results from the {current_year} NBA season.")
        predictResults(current_year)
    elif inpt == 3:
        print("Single Team Simulation coming soon...")
    else:
        print("Menu item not found. Please choose an item from our menu.")


startProg()
