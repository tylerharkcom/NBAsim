import csv
import random as rnd
import pandas as pd
import statistics

current_year = 2020

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


def startProg():
    valid_teams = ["TOR", "BOS", "PHI", "BRK", "NYK", "MIL", "IND", "CHI", "DET", "CLE", "MIA", "ORL", "WAS", "CHO", "ATL", "DEN", "OKC", "UTA", "POR", "MIN", "LAL", "LAC", "SAC", "PHO", "GSW", "HOU", "DAL", "MEM", "NOP", "SAS"]
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
        output.append(getTeamPoints(2020, team))
    team1stats = output[0]
    team2stats = output[1]
    gamesSim(team1, team2, team1stats, team2stats, num)


startProg()
