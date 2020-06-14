import csv
import math

team_list = ['OBY', 'R', 'PK', 'SSG', 'SNG', 'GHOST', 'EUN', 'RNG']
ELO_list = {}
form_list = {}

for team in team_list: 
    ELO_list.update({team:1500})
    form_list.update({team:0})

#start_date = '4/4/2020'
#end_date = '6/7/2020'
k_factor = 40
contested_set_modifier = 2/3
dominant_set_modifier = 4/3
playoffs_games_per_set = 5

reg_season_saved = False

#print("k =", k_factor)
#print("partial credit =", contested_set_modifier)
#print("3-0 Bonus =", clean_sweep_modifier)

class Match:
    def __init__(self, date, home, away, result): 
        self.date = date
        self.home = home
        self.away = away
        self.home_elo = ELO_list[home]
        self.away_elo = ELO_list[away]
        
        if result == "2-0": 
            self.result = "2-0"
            self.winner = home
            self.loser = away
        elif result == "2-1": 
            self.result = "2-1"
            self.winner = home
            self.loser = away
        elif result  == "0-2": 
            self.result = "0-2"
            self.winner = away
            self.loser = home
        elif result == "1-2": 
            self.result = "1-2"
            self.winner = away
            self.loser = home
        elif result == "3-0":
            self.result = "3-0"
            self.winner = home
            self.loser = away
        elif result == "3-1":
            self.result = "3-1"
            self.winner = home
            self.loser = away
        elif result == "3-2":
            self.result = "3-2"
            self.winner = home
            self.loser = away
        elif result == "0-3":
            self.result = "0-3"
            self.winner = away
            self.loser = home
        elif result == "1-3":
            self.result = "1-3"
            self.winner = away
            self.loser = home
        elif result == "2-3":
            self.result = "2-3"
            self.winner = away
            self.loser = home
        else: 
            self.result = "x-x"
            self.winner = "HIREZ"
            self.loser = "HIREZ"
    def printMatch(self): 
        print(self.home, self.result, self.away)
        
def updateELO(match): 
        home = match.home
        away = match.away
        
        home_elo = match.home_elo
        away_elo = match.away_elo
        
        #calculate expected scores based on current ratings. Values between 0 and 1
        home_expected = 1/(1+math.pow(10,(away_elo-home_elo)/400))
        away_expected = 1/(1+math.pow(10,(home_elo-away_elo)/400))
        
        if match.winner == home: 
            #home team won
            #print("home win")
            if match.result == "2-0":
                #full marks for a sweep
                new_home = round(home_elo+k_factor*(1-home_expected),2)
                new_away = round(away_elo+k_factor*(0-away_expected),2)
            elif match.result == "2-1": 
                #partial credit for 2-1
                new_home = round(home_elo+contested_set_modifier*k_factor*(1-home_expected),2)
                new_away = round(away_elo+contested_set_modifier*k_factor*(0-away_expected),2)
            elif match.result == "3-0":
                new_home = round(home_elo+dominant_set_modifier*k_factor*(1-home_expected),2)
                new_away = round(away_elo+dominant_set_modifier*k_factor*(0-away_expected),2)
            elif match.result == "3-1":
                new_home = round(home_elo+k_factor*(1-home_expected),2)
                new_away = round(away_elo+k_factor*(0-away_expected),2)
            elif match.result == "3-2":
                new_home = round(home_elo+contested_set_modifier*k_factor*(1-home_expected),2)
                new_away = round(away_elo+contested_set_modifier*k_factor*(0-away_expected),2)
            else: 
                print("error")
        elif match.winner == away: 
            #away team won
            #print("away win")
            if match.result == "0-2": 
                new_home = round(home_elo+k_factor*(0-home_expected),2)
                new_away = round(away_elo+k_factor*(1-away_expected),2)
            elif match.result == "1-2": 
                new_home = round(home_elo+contested_set_modifier*k_factor*(0-home_expected),2)
                new_away = round(away_elo+contested_set_modifier*k_factor*(1-away_expected),2)
            elif match.result == "0-3":
                new_home = round(home_elo+k_factor*dominant_set_modifier*(0-home_expected),2)
                new_away = round(away_elo+k_factor*dominant_set_modifier*(1-away_expected),2)
            elif match.result == "1-3":
                new_home = round(home_elo+k_factor*(0-home_expected),2)
                new_away = round(away_elo+k_factor*(1-away_expected),2)
            elif match.result == "2-3":
                new_home = round(home_elo+contested_set_modifier*k_factor*(0-home_expected),2)
                new_away = round(away_elo+contested_set_modifier*k_factor*(1-away_expected),2)
            else: 
                print("error")
        else: 
            #print("bad result")
            new_home = home_elo
            new_away = away_elo
            
        ELO_list.update({home:new_home})
        ELO_list.update({away:new_away})

def makePrediction(home, away):
    home_elo = ELO_list[home]
    away_elo = ELO_list[away]

    home_expected = 1/(1+math.pow(10,(away_elo-home_elo)/400))
    away_expected = 1/(1+math.pow(10,(home_elo-away_elo)/400))
    #print(home, "("+ str(home_elo)+ ")", str(round(100*home_expected,2))+"%", away, "("+ str(away_elo)+ ")", str(round(100*away_expected,2))+"%")

    #Alternate way to calculate set results
    # home_games = round(home_expected*playoffs_games_per_set,2)
    # away_games = round(away_expected*playoffs_games_per_set,2)

    if home_expected <= 0.4: 
        home_games = 0
        away_games = 3
    elif home_expected > 0.4 and home_expected <= 0.45:
        home_games = 1
        away_games = 3
    elif home_expected > 0.45 and home_expected <= 0.5: 
        home_games = 2
        away_games = 3
    elif home_expected > 0.5 and home_expected <= 0.55: 
        home_games = 3
        away_games = 2
    elif home_expected > 0.55 and home_expected <= 0.6:
        home_games = 3
        away_games = 1
    else:
        home_games = 3
        away_games = 0

    return(home+" "+str(home_games)+"-"+str(away_games)+" "+away)

predictions = []

with open("SPL_Results_2020.csv", newline='') as datafile: 
    gamereader = csv.DictReader(datafile, fieldnames=['Date','Home','Away','Result'])

    for row in gamereader:
        if row['Result'] is not None:
            tmp = Match(row['Date'], row['Home'], row['Away'], row['Result'])
            #tmp.printMatch()
            #save a copy of the final regular season rankings
            if row['Date'] == "6/12/2020" and reg_season_saved == False:
                reg_season_saved = True
                final_reg_season_rankings = ELO_list.copy()

            updateELO(tmp)
            #print(ELO_list)
        else: 
            prediction = makePrediction(row['Home'],row['Away'])
            predictions.append(prediction)

print("Regular Season Rankings:")
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

print("Playoff Predictions")
for match in predictions:
    print(match)
