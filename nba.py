# Tyler Harkcom
# Developed in 2020

# Simple CSV file reader that takes nba_elo.csv files from FiveThirtyEight (https://github.com/fivethirtyeight/data/tree/master/nba-forecasts)
# and produces a game-by-game summary of a user-inputted year's NBA results, given
# a year between 1946 and 2020. Standings are tabulated and saved in a dictionary.

# Things to add:
# 1. Support for playoffs -- round-by-round breakdowns, announcing series winners, etc.
# 2. Sorting of standings by wins -- being able to determine playoff seeding based on end-of-year record
# 3. Game prediction/simulation using elo_predictions on csv file -- randomly simulate (the rest of) the season using 538's predictions
# 4. Make things object-oriented and more modular for ease of translation between files

import csv
import random as rnd
import statistics

current_year = 2020

valid_teams = ["TOR", "BOS", "PHI", "BRK", "NYK", "MIL", "IND", "CHI", "DET", "CLE", "MIA", "ORL", "WAS", "CHO", "ATL", "DEN", "OKC", "UTA", "POR", "MIN", "LAL", "LAC", "SAC", "PHO", "GSW", "HOU", "DAL", "MEM", "NOP", "SAS"]

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


def getTeamPoints(yr, tm):
    with open('nba_elo.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        # target_year = int(input("Get NBA results for which year?"))
        team = tm
        target_year = yr
        team_score = []
        opp_score = []
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
                    team2 = row[5]

                    if row[22] == '' or row[23] == '':# Game hasn't been played yet
                        line_count += 1

                    else:
                        if team1 == team:
                            team_score.append(int(row[22]))
                            opp_score.append(int(row[23]))
                        elif team2 == team:
                            team_score.append(int(row[23]))
                            opp_score.append(int(row[22]))
                        else:
                            line_count += 1

        team_avg = statistics.mean(team_score)
        team_std = statistics.stdev(team_score)
        opp_avg = statistics.mean(opp_score)
        opp_std = statistics.stdev(opp_score)

        # print("here")
        return [team_avg, team_std, opp_avg, opp_std]

def gameSim(team1, team2):
    team1_pts = team1[0]
    team1_std = team1[1]
    team1_opp_pts = team1[2]
    team1_opp_std = team1[3]
    team2_pts = team2[0]
    team2_std = team2[1]
    team2_opp_pts = team2[2]
    team2_opp_std = team2[3]

    team1_score = (rnd.gauss(team1_pts,team1_std) + rnd.gauss(team1_opp_pts,team1_opp_std))
    team2_score = (rnd.gauss(team2_pts,team2_std) + rnd.gauss(team2_opp_pts,team2_opp_std))

    if (int(round(team1_score)) > int(round(team2_score))):
        return 1
    elif (int(round(team1_score)) < int(round(team2_score))):
        return -1
    else:
        return 0

def gamesSim(name1, name2, team1, team2, num):
    gamesout = []
    team1win = 0
    team2win = 0
    tie = 0
    for i in range(num):
        gm = gameSim(team1, team2)
        gamesout.append(gm)
        if gm == 1:
            team1win += 1
        elif gm == -1:
            team2win += 1
        else: tie += 1
    print(name1, 'win: ', round(team1win/(team1win+team2win+tie)*100),'%')
    print(name2, 'win: ', round(team2win/(team1win+team2win+tie)*100),'%')
    print('Tie: ', round(tie/(team1win+team2win+tie)*100),'%')
    return gamesout


def startSimProg(year):
    print("Welcome to the NBA Series Simulator. Enter the three-letter abbreviation of Team 1. (Example: Boston = BOS, New York Knicks = NYK)")
    team1 = str(input())
    while team1 not in valid_teams:
        print("Invalid team. Please try again.")
        print("Enter the three-letter abbreviation of Team 1. (Example: Boston = BOS, New York Knicks = NYK)")
        team1 = str(input())
    print("Enter the three-letter abbreviation of Team 2. (Example: Boston = BOS, New York Knicks = NYK)")
    team2 = str(input())
    while team2 not in valid_teams:
        print("Invalid team. Please try again.")
        print("Enter the three-letter abbreviation of Team 2. (Example: Boston = BOS, New York Knicks = NYK)")
        team2 = str(input())
    print("How many simulated games would you like to run?")
    num = int(input())
    teams = [team1, team2]
    output = []
    for team in teams:
        output.append(getTeamPoints(year, team))
    team1stats = output[0]
    team2stats = output[1]
    gamesSim(team1, team2, team1stats, team2stats, num)

def startProg():
    print("Welcome to [Untitled NBA Predictor]. Please select a program to continue: ")
    print("1: NBA Historical Records, 2: Current NBA Season Simulator, 3: Series Simulation")
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
        print("Which year would you like to simulate in? Please enter a year from 1947 to 2020")
        year = int(input())
        startSimProg(year)
    else:
        print("Menu item not found. Please choose an item from our menu.")


startProg()
