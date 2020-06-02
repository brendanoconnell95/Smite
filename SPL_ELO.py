import csv
import math

team_list = ['OBY', 'R', 'PK', 'SSG', 'SNG', 'GHOST', 'EUN', 'RNG']
ELO_list = {}
for team in team_list: 
    ELO_list.update({team:1500})

#start_date = '4/4/2020'
#end_date = '6/7/2020'
k_factor = 40
three_game_set_credit = 3/4
print("k =", k_factor)
print("partial credit =", three_game_set_credit)

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
                new_home = round(home_elo+three_game_set_credit*k_factor*(1-home_expected),2)
                new_away = round(away_elo+three_game_set_credit*k_factor*(0-away_expected),2)
            else: 
                print("error")
        elif match.winner == away: 
            #away team won
            #print("away win")
            if match.result == "0-2": 
                new_home = round(home_elo+k_factor*(0-home_expected),2)
                new_away = round(away_elo+k_factor*(1-away_expected),2)
            elif match.result == "1-2": 
                new_home = round(home_elo+three_game_set_credit*k_factor*(0-home_expected),2)
                new_away = round(away_elo+three_game_set_credit*k_factor*(1-away_expected),2)
            else: 
                print("error")
        else: 
            #print("bad result")
            new_home = home_elo
            new_away = away_elo
            
        ELO_list.update({home:new_home})
        ELO_list.update({away:new_away})

with open("SPL_Results_2020.csv", newline='') as datafile: 
    gamereader = csv.DictReader(datafile, fieldnames=['Date','Home','Away','Result'])

    for row in gamereader:
        tmp = Match(row['Date'], row['Home'], row['Away'], row['Result'])
        #tmp.printMatch()
        updateELO(tmp)
    for elem in sorted(ELO_list.items(), key=lambda x: x[1], reverse=True): 
        print(elem)


        
        
        
        
        
        
        
        
        
        
        