# Author: Nick Konz
import pandas as pd
import os
import sqlite3
import datetime

# from databaseManager.py:
def createMasterTable(reset=True):  # Reset=True will fill 0 into the data table
    cursor = conn.cursor()
    try:
        cursor.execute('CREATE TABLE master (gameCount INTEGER)')
    except sqlite3.OperationalError:    # The table already exists -- do nothing
        pass
    finally:
        if reset:
            cursor.execute('DELETE FROM master WHERE gameCount > -1')   # Deletes everything (not very pretty but it works)
            cursor.execute('INSERT INTO master(gameCount) SELECT 0')
        conn.commit()

def createGameTable():
    cursor = conn.cursor()
    try:
        cursor.execute("""CREATE TABLE games (
                        timestamp TEXT,
                        gameID INTEGER,
                        player1 TEXT,
                        player2 TEXT,
                        player3 TEXT,
                        player4 TEXT,
                        player5 TEXT,
                        player6 TEXT,
                        player7 TEXT,
                        player8 TEXT
                        )""")
    except sqlite3.OperationalError:    # The table already exists -- do nothing
        pass
    finally:
        conn.commit()

# Creates a table for the given player tag that stores data from each game
def createPlayerTable(playerName):
    # import pdb
    # pdb.set_trace()
    cursor = conn.cursor()
    try:
        # Create the table if it doesn't already exist
        cursor.execute("""CREATE TABLE [{}] (
                        timestamp TEXT,
                        gameID INTEGER,
                        charName TEXT,
                        rank INTEGER,
                        damage INTEGER
                        )""".format(playerName))
    except sqlite3.OperationalError:    # Table already exists
        pass
    finally:
        conn.commit()



curDir = os.path.dirname(__file__)
dataPath = os.path.join(curDir, 'testGames.db')
conn = sqlite3.connect(dataPath)    # Stores the connection to the database

if __name__ == "__main__":
    df = pd.read_csv('exampleData.csv')

    # get all player names
    allPlayerNames = []
    for entry in df['KO counts']:
        li = entry.split(" ")
        for l in li:
            m = l.split(":")
            name = m[0]
            if name not in allPlayerNames:
                allPlayerNames.append(name)

    createMasterTable()
    createGameTable()
    for name in allPlayerNames:
        createPlayerTable(name)

    # log each game
    for index, row in df.iterrows():
        # master TABLE
        cursor = conn.cursor()
        gameID = int(row['game no.'])
        command = """INSERT INTO master VALUES ({})""".format(gameID)
        cursor.execute(command)


        # games TABLE 
        now = datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')

        # Iterate through the players in the game and define the ones that are present
        allPlayers = ['#'] * 8              # Fill a list with the default empty value '#'

        li = row['KO counts'].split(" ")
        i = 0
        for l in li:
            m = l.split(":")
            name = m[0]
            allPlayers[i] = name
            i += 1

        # Execute the command storing the tags of each player, or '#' if empty
        command = """INSERT INTO games VALUES ('{}', {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(
        now, gameID, allPlayers[0], allPlayers[1], allPlayers[2], allPlayers[3], allPlayers[4], allPlayers[5], allPlayers[6], allPlayers[7])
        cursor.execute(command)


        # players TABLES
        playerDamages = {}

        li = row['Damage percentages'].split(" ")
        i = 0
        for l in li:
            m = l.split(":")
            playerDamages[m[0]] = m[1]

        for player in [p for p in allPlayers if p != "#"]:

            rank = 1 if row['winner name'] == player else 0

            # print(player)

            command = """INSERT INTO [{}] VALUES ('{}', {}, '{}', {}, {})""".format(
                player, now, gameID, "#", rank, int(playerDamages[player]))   # Use randomized dmg for now
            cursor.execute(command)
    
        conn.commit()





    # with conn:
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM BEEF")
    #     print(cursor.fetchall())