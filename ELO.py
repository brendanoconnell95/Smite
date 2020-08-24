import math

k_factor = 40

contested_set_modifier = 2/3
dominant_set_modifier = 4/3
playoffs_games_per_set = 5

#print("k =", k_factor)
#print("partial credit =", contested_set_modifier)
#print("3-0 Bonus =", clean_sweep_modifier)

class Match:
    def __init__(self, date, home, away, result): 
        self.date = date
        self.home = home
        self.away = away
        
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
        
def updateELO(match, home_elo, away_elo): 
        home = match.home
        away = match.away
        
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
            
        return (new_home, new_away)

def makePrediction(home, away, playoffs):
    home_elo = ELO_list[home]
    away_elo = ELO_list[away]

    home_expected = 1/(1+math.pow(10,(away_elo-home_elo)/400))
    away_expected = 1/(1+math.pow(10,(home_elo-away_elo)/400))
    #print(home, "("+ str(home_elo)+ ")", str(round(100*home_expected,2))+"%", away, "("+ str(away_elo)+ ")", str(round(100*away_expected,2))+"%")

    #Alternate way to calculate set results
    # home_games = round(home_expected*playoffs_games_per_set,2)
    # away_games = round(away_expected*playoffs_games_per_set,2)

    if home_expected <= 0.4: 
        if playoffs:
            home_games = 0
            away_games = 3
        else: 
            home_games = 0
            away_games = 2
    elif home_expected > 0.4 and home_expected <= 0.45:
        if playoffs: 
            home_games = 1
            away_games = 3
        else: 
            home_games = 1
            away_games = 2
    elif home_expected > 0.45 and home_expected <= 0.5: 
        if playoffs: 
            home_games = 2
            away_games = 3
        else: 
            home_games = 1
            away_games = 2
    elif home_expected > 0.5 and home_expected <= 0.55: 
        if playoffs: 
            home_games = 3
            away_games = 2
        else: 
            home_games = 2
            away_games = 1
    elif home_expected > 0.55 and home_expected <= 0.6:
        if playoffs: 
            home_games = 3
            away_games = 1
        else: 
            home_games = 2
            away_games = 1
    else:
        if playoffs: 
            home_games = 3
            away_games = 0
        else: 
            home_games = 2
            away_games = 0

    return("("+str(round(100*home_expected,2))+"%) "+home+" "+str(home_games)+"-"+str(away_games)+" "+away+" ("+str(round(100*away_expected,2))+"%)")