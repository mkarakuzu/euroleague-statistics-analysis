#libraries
import requests
import pandas as pd
import time

try:
    game_count = 1  #game counter
    data = pd.DataFrame()  #main dataframe to store all games
    seasoncode = "E2025"

    while game_count <= 35:  #loop for 35 games
        response = requests.get(f"https://live.euroleague.net/api/Points?gamecode={game_count}&seasoncode={seasoncode}", timeout = 10)  #get json from api
        time.sleep(0.25)  #delay to be polite

        newdata = response.json()  #convert response to json
        df = pd.DataFrame(newdata["Rows"])  #create dataframe from json

        df["GAME_CODE"] = game_count  #add game code column
        df["SEASON_CODE"] = "E2025"  #add season code column
        df["TEAM"] = df["TEAM"].str.upper().str.strip()  #clean and normalize team names
        
        data = pd.concat([data, df])  #append new game data
        game_count += 1  #increase game counter

    all_games_df = data  #final combined dataframe
    
except Exception:  #error handling
    print(f"Error: {Exception}")  #print error info

#per-game means
total_points = all_games_df.groupby("TEAM")["POINTS"].sum()  #total points by team
game_count_all = all_games_df.groupby("TEAM")["GAME_CODE"].nunique()  #unique games per team
scores_per_game = (total_points / game_count_all).reset_index(name = "AVG_SCORES_PER_GAME")  #avg score per game

ulk_per_game_score = scores_per_game[scores_per_game["TEAM"] == "ULK"]["AVG_SCORES_PER_GAME"].iloc[0]  #ulk avg points
ist_per_game_score = scores_per_game[scores_per_game["TEAM"] == "IST"]["AVG_SCORES_PER_GAME"].iloc[0]  #ist avg points
avg_per_game_score = scores_per_game["AVG_SCORES_PER_GAME"].mean()  #league avg points
best_team_score_name = scores_per_game[scores_per_game["AVG_SCORES_PER_GAME"] == scores_per_game["AVG_SCORES_PER_GAME"].max()]["TEAM"].iloc[0]  #best team name
best_team_score = scores_per_game["AVG_SCORES_PER_GAME"].max()  #best avg score

#conceded
ptsab_for_all_teams = all_games_df.groupby(["TEAM", "GAME_CODE"])[["POINTS_A", "POINTS_B"]].max()  #total points in game
pts_for_all_teams = all_games_df.groupby(["TEAM", "GAME_CODE"])["POINTS"].sum()  #team's own points
total_ab = ptsab_for_all_teams["POINTS_A"] + ptsab_for_all_teams["POINTS_B"]  #total points in match
conceded_per_game = total_ab - pts_for_all_teams  #points conceded
total_conceded_points = conceded_per_game.groupby("TEAM").sum()  #total conceded points
avg_conceded_per_game = (total_conceded_points / game_count_all).reset_index(name = "AVG_CONCEDED_PER_GAME")  #avg conceded per game

ulk_conceded_per_game = avg_conceded_per_game[avg_conceded_per_game["TEAM"] == "ULK"]["AVG_CONCEDED_PER_GAME"].iloc[0]  #ulk avg conceded
ist_conceded_per_game = avg_conceded_per_game[avg_conceded_per_game["TEAM"] == "IST"]["AVG_CONCEDED_PER_GAME"].iloc[0]  #ist avg conceded
avg_per_game_conceded = avg_conceded_per_game["AVG_CONCEDED_PER_GAME"].mean()  #league avg conceded
best_team_conceded_name = avg_conceded_per_game[avg_conceded_per_game["AVG_CONCEDED_PER_GAME"] == avg_conceded_per_game["AVG_CONCEDED_PER_GAME"].min()]["TEAM"].iloc[0]  #best defense team name
best_team_conceded_points = avg_conceded_per_game["AVG_CONCEDED_PER_GAME"].min()  #best defense avg

#3pt and 2pt numbers
all_3pt = all_games_df[all_games_df["ACTION"] == "Three Pointer"].groupby("TEAM")["POINTS"].sum()  #total 3pt points
all_2pt = all_games_df[all_games_df["ACTION"] == "Two Pointer"].groupby("TEAM")["POINTS"].sum()  #total 2pt points
per_game_3pt = (all_3pt / game_count_all).reset_index(name = "AVG_3PT")  #avg 3pt per game
per_game_2pt = (all_2pt / game_count_all).reset_index(name = "AVG_2PT")  #avg 2pt per game

ulk_3pt = per_game_3pt[per_game_3pt["TEAM"] == "ULK"]["AVG_3PT"].iloc[0]  #ulk 3pt avg
ist_3pt = per_game_3pt[per_game_3pt["TEAM"] == "IST"]["AVG_3PT"].iloc[0]  #ist 3pt avg
avg_3pt = per_game_3pt["AVG_3PT"].mean()  #league avg 3pt
best_team_3pt_name = per_game_3pt[per_game_3pt["AVG_3PT"] == per_game_3pt["AVG_3PT"].max()]["TEAM"].iloc[0]  #best 3pt team
best_team_3pt = per_game_3pt["AVG_3PT"].max()  #best 3pt avg

ulk_2pt = per_game_2pt[per_game_2pt["TEAM"] == "ULK"]["AVG_2PT"].iloc[0]  #ulk 2pt avg
ist_2pt = per_game_2pt[per_game_2pt["TEAM"] == "IST"]["AVG_2PT"].iloc[0]  #ist 2pt avg
avg_2pt = per_game_2pt["AVG_2PT"].mean()  #league avg 2pt
best_team_2pt_name = per_game_2pt[per_game_2pt["AVG_2PT"] == per_game_2pt["AVG_2PT"].max()]["TEAM"].iloc[0]  #best 2pt team
best_team_2pt = per_game_2pt["AVG_2PT"].max()  #best 2pt avg

#FASTBREAK Points
fastbreak_pts = all_games_df[all_games_df["FASTBREAK"] == "1"].groupby("TEAM")["POINTS"].sum()  #total fastbreak points
fastbreak_avg = (fastbreak_pts / game_count_all).reset_index(name = "AVG_FASTBREAK_POINTS")  #avg fastbreak per game

ulk_fastbreak = fastbreak_avg[fastbreak_avg["TEAM"] == "ULK"]["AVG_FASTBREAK_POINTS"].iloc[0]  #ulk fastbreak avg
ist_fastbreak = fastbreak_avg[fastbreak_avg["TEAM"] == "IST"]["AVG_FASTBREAK_POINTS"].iloc[0]  #ist fastbreak avg
avg_fastbreak = fastbreak_avg["AVG_FASTBREAK_POINTS"].mean()  #league avg fastbreak
best_team_fastbreak_name = fastbreak_avg[fastbreak_avg["AVG_FASTBREAK_POINTS"] == fastbreak_avg["AVG_FASTBREAK_POINTS"].max()]["TEAM"].iloc[0]  #best fastbreak team
best_team_fastbreak = fastbreak_avg["AVG_FASTBREAK_POINTS"].max()  #best fastbreak avg

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(5)  #x-axis positions for bars
ulk_list = [ulk_per_game_score, ulk_conceded_per_game, ulk_3pt, ulk_2pt, ulk_fastbreak]  #ulk stats
ist_list = [ist_per_game_score, ist_conceded_per_game, ist_3pt, ist_2pt, ist_fastbreak]  #ist stats
avg_list = [avg_per_game_score, avg_per_game_conceded, avg_3pt, avg_2pt, avg_fastbreak]  #league avg stats
best_list = [best_team_score, best_team_conceded_points, best_team_3pt, best_team_2pt, best_team_fastbreak]  #best team stats

width = 0.2  #bar width
center_position = x + 1.5 * width  #x tick positions
plt.figure(figsize = (16,10))  #figure size

bar1 = plt.bar(x, ulk_list, width, color = 'yellow')  #ulk bars
bar2 = plt.bar(x + 0.2, ist_list, width, color = 'blue')  #ist bars
bar3 = plt.bar(x + 0.4, avg_list, width, color = 'orange')  #avg bars
bar4 = plt.bar(x + 0.6, best_list, width, color = 'green')  #best team bars

plt.bar_label(bar1, fmt = '%.1f')  #label ulk values
plt.bar_label(bar2, fmt = '%.1f')  #label ist values
plt.bar_label(bar3, fmt = '%.1f')  #label avg values
plt.bar_label(bar4, labels = [f'{best_team_score_name}\n{best_team_score:.1f}',  #custom label: team + value
                               f'{best_team_conceded_name}\n{best_team_conceded_points:.1f}',
                                 f'{best_team_3pt_name}\n{best_team_3pt:.1f}',
                                   f'{best_team_2pt_name}\n{best_team_2pt:.1f}',
                                     f'{best_team_fastbreak_name}\n{best_team_fastbreak:.1f}'])

plt.xticks(center_position, ["Score per match", "Points conceded per match", "3PT points per match", "2PT points per match", "Fast Break points per match"], rotation = 15)  #x labels
plt.ylabel("Per-match value")  #y-axis label

plt.legend(["ULK", "IST", "League AVG", "Best Team"])  #legend

plt.show()  #show chart

playerlist_3pt = all_games_df[all_games_df["ACTION"] == "Three Pointer"].groupby(["TEAM", "PLAYER"])["POINTS"].sum().sort_values(ascending = False)  #total 3pt points by team and player
playerlist_3pt_avg = (playerlist_3pt / game_count_all).reset_index(name = "AVG_3PT")  #avg 3pt per game
playerlist_3pt_avg = playerlist_3pt_avg.sort_values(by="AVG_3PT", ascending=False)  #sort by avg 3pt desc
playerlist_3pt_avg = playerlist_3pt_avg[playerlist_3pt_avg["AVG_3PT"] >= 6.0]  #filter players avg >= 6
playerlist_3pt_avg = playerlist_3pt_avg[playerlist_3pt_avg["TEAM"] != "ULK"].reset_index(drop=True)  #exclude ulk team

print(playerlist_3pt_avg.head())  #print top players