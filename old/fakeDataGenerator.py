#----- Author: Nick Konz -----#
import argparse
from argparse import RawTextHelpFormatter
import pandas as pd
import random as rd

PLAYERS = ("BEEF", "sivad", "Thomato", "postmabone", "curt", "LONG", "raki", "rupa")

def generateMatches(N):
    prevData = pd.read_csv("exampleData.csv")
    lastgameNo = prevData['game no.'].values[-1]


    f = open("exampleData.csv", "a")

    for n in range(N):
        line = ""

        #game number
        line += str(lastgameNo + 1 + n) + "," #game number

        #winner
        line += rd.choice(PLAYERS) + ","

        #KO counts
        playerCount = rd.randrange(2, 9)
        players = rd.sample(PLAYERS, playerCount)
        maxKOCount = (playerCount - 1) * 3
        for i, player in enumerate(players):
            line += player + ":"
            KOs = round(rd.gauss(maxKOCount / 2, 1*(playerCount - 1))) #draws KO count from a normal dist centered at half of the max KOs you can get
            if KOs < 0:
                KOs = 0
            if KOs > maxKOCount:
                KOs = maxKOCount
            line += str(KOs) #random amount of KOs
            if i < (len(players) - 1):
                line += " "

        line += ","

        #Damage Percentages
        for i, player in enumerate(players):
            line += player + ":"
            dam = round(rd.gauss((maxKOCount * 100) / 2, 100*(playerCount - 1)))
            if dam < 0:
                dam = 0
            line += str(dam) #random amount of KOs
            if i < (len(players) - 1):
                line += " "
        line += "\n"

        f.write(line)

    f.close()
    return;

def main():

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("N", type=str, help="number of matches generated")
    
    args = parser.parse_args()
    N = args.N
    generateMatches(int(N))
    
main()