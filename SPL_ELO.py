import csv

from ELO import *

team_list = ['OBY', 'R', 'PK', 'SSG', 'SNG', 'GHOST', 'EUN', 'RNG']
ELO_list = {}
form_list = {}

for team in team_list: 
    ELO_list.update({team:1500})
    form_list.update({team:0})

reg_season_saved = False

predictions = []

with open("phase_one_results_2020.csv", newline='') as datafile: 
    gamereader = csv.DictReader(datafile, fieldnames=['Date','Home','Away','Result'])

    for row in gamereader:
        if row['Result'] is not None:
            tmp = Match(row['Date'], row['Home'], row['Away'], row['Result'])
            #tmp.printMatch()
            #save a copy of the final regular season rankings
            if row['Date'] == "6/12/2020" and reg_season_saved == False:
                reg_season_saved = True
                final_reg_season_rankings = ELO_list.copy()

            home_elo = ELO_list[tmp.home]
            away_elo = ELO_list[tmp.away]
            res = updateELO(tmp, home_elo, away_elo)
            
            ELO_list.update({tmp.home:res[0]})
            ELO_list.update({tmp.away:res[1]})
            #print(ELO_list)
        else: 
            prediction = ELO.makePrediction(row['Home'],row['Away'])
            predictions.append(prediction)

print("Phase 1 Rankings:")
for elem in sorted(final_reg_season_rankings.items(), key=lambda x: x[1], reverse=True): 
    print(elem)
print()

playoff_changes = {}
for team in team_list:
    playoff_changes.update({team:0})

for team in final_reg_season_rankings:
    reg = final_reg_season_rankings[team]
    cur = ELO_list[team]
    diff = round(cur-reg,2)
    playoff_changes.update({team:diff})

print("Playoff changes")
for elem in sorted(final_reg_season_rankings.items(), key=lambda x: x[1], reverse=True): 
    print(elem[0], round(playoff_changes[elem[0]],2), "("+str(round(elem[1]+playoff_changes[elem[0]],2))+")")
print()

if predictions != []: 
    print("Playoff Predictions")
    for match in predictions:
        print(match)
