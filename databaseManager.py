import sqlite3
import os
import numpy as np
import datetime
import copy
from collections import OrderedDict

from IconClassifier.iconModel import charDict       # Needed to run statistics on every character
from textRecognition.game import makeSampleGame     # Used to populate the database with sample data

curDir = os.path.dirname(__file__)
dataPath = os.path.join(curDir, 'gameLog.db')
conn = sqlite3.connect(dataPath)    # Stores the connection to the database

# ======== Functions to create new tables -- automatically called on every use to be safe =======================

# We'll have one table that stores general information about the configuration, such as number of games played
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
    cursor = conn.cursor()
    try:
        # Create the table if it doesn't already exist
        cursor.execute("""CREATE TABLE {} (
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


# ================================ Functions to store new records ==================================

def logGame(game, gameID):
    createGameTable()
    cursor = conn.cursor()
    now = datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')

    # Iterate through the players in the game and define the ones that are present
    allPlayers = ['#'] * 8              # Fill a list with the default empty value '#'
    for i in range(len(game.players)):  # Replace '#' with the actual player's tag where applicable
        allPlayers[i] = game.players[i].tag

    # Execute the command storing the tags of each player, or '#' if empty
    command = """INSERT INTO games VALUES ('{}', {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(
    now, gameID, allPlayers[0], allPlayers[1], allPlayers[2], allPlayers[3], allPlayers[4], allPlayers[5], allPlayers[6], allPlayers[7])
    cursor.execute(command)
    conn.commit()


# Takes a player object as input and logs relevant information
def logPlayer(player, gameID):
    createPlayerTable(player.tag)   # Make sure that we have a table created for the player
    cursor = conn.cursor()
    now = datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
    command = """INSERT INTO {} VALUES ('{}', {}, '{}', {}, {})""".format(
    player.tag, now, gameID, player.charName, player.rank, np.random.randint(0, 200))
    cursor.execute(command)
    conn.commit()


# Store all of the relevant results for the game -- stores a record of the game and updates each player's page``````
def logResults(game):
    # Retrieve the current number of games and increment immediately
    gameID = getGameCount()
    incrementGameCount()

    # Update the stats for each player in the game
    for player in game.players:
        logPlayer(player, gameID)
    logGame(game, gameID)   # Record the time, gameID, and players in the game
    conn.commit()


# =========================== Functions to fetch and interpret existing results ============================

# Returns the total number of games played -- stored in the master sheet in the database
def getGameCount():
    createMasterTable(reset=False)  # Check that the table is created without reseting anything
    cursor = conn.cursor()
    cursor.execute('SELECT gameCount FROM master')
    count = cursor.fetchone()[0]
    return count


def incrementGameCount():
    createMasterTable(reset=False)
    count = getGameCount()  # Retrieve the current number of games played
    cursor = conn.cursor()
    try:
        # Update the games played field, incrementing by one
        cursor.execute('UPDATE master SET gameCount = "{}" WHERE gameCount = "{}"'.format(count + 1, count)) # Delete the old count
        conn.commit()
    except sqlite3.OperationalError:
        print('Error with incrementing value')


# Returns information about a player's results in the given game
def getPlayerResultsFromID(playerTag, gameID):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM {} where gameID = {}'.format(playerTag, gameID))
    return cursor.fetchone()  # Returns None if the player was not in the game


# Returns the information about which players played in the given game
def getGameFromID(gameID):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM games where gameID = {}'.format(gameID))
    return cursor.fetchone()


# Simply returns the total number of games that the given player has won
def countAllWins(playerTag):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM {} WHERE rank = 1'.format(playerTag))
    wins = cursor.fetchall()
    return len(wins)


# Returns a list of tuples with each of the games where the player won with the given character
def findWinsWithCharacter(playerTag, charName):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM {} WHERE rank = 1 AND charName = "{}"'.format(playerTag, charName))
    wins = cursor.fetchall()
    return wins


# Returns the win ratio for the given player and character
def getWinRatio(playerTag, charName):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM {} WHERE charName = "{}"'.format(playerTag, charName))
    allGames = cursor.fetchall()
    if len(allGames) == 0:    # If no games have been played, give a ratio of 0
        return 0

    wonGames = findWinsWithCharacter(playerTag, charName)
    return len(wonGames) / len(allGames)



# Returns a sorted dictionary with characters as the keys and win ratios as the values
def getAllWinRatios(playerTag):
    outDict = copy.deepcopy(charDict)  # Creates a copy of the dictionary
    for charName in outDict.keys():
        ratio = getWinRatio(playerTag, charName)
        outDict[charName] = ratio
    return outDict


# Returns the number of games won by a player with a given character
def countWinsWithCharacter(playerTag, charName):
    return len(findWinsWithCharacter(playerTag, charName))


# Returns TRUE if the player was involved in the given game
def gameContainsPlayer(gameID, playerTag):
    results = getGameFromID(gameID)
    i = 2   # Skip over the timestamp & ID, iterate over all players
    while i < len(results) and results[i] != '#':
        if results[i] == playerTag:
            return True
        i += 1
    return False


# Counts the number of games where player1 playing character1 beat player2 playing character2
# TODO: Modify to count not only wins but other ranks for multiplayer
def getMatchupStats(playerTag_1, charName_1, playerTag_2, charName_2):
    allWins = 0
    allMatchups = 0
    p1_wins = findWinsWithCharacter(playerTag_1, charName_1)    # All of the games where p1 won with the character
    for win in p1_wins:
        gameID = win[1]
          # Look up the won game in the master database to find the other players

        if gameContainsPlayer(gameID, playerTag_2):    # If the other player was in the game
            allMatchups += 1
            p2_result = getPlayerResultsFromID(playerTag_2, gameID)
            p2_char = p2_result[2]
            if p2_char == charName_2:
                allWins += 1
    if allMatchups == 0:
        print('This matchup never occured')
    return (allWins, allMatchups)   # Return a tuple with the number of wins and the total games played


def generateSampleData(numGames):
    import pdb
    pdb.set_trace()
    for log in range(numGames):
        numPlayers = np.random.randint(1, 4)
        sampleGame = makeSampleGame(numPlayers)
        logResults(sampleGame)


if __name__ == '__main__':
    #print(getGameCount())
    # generateSampleData(1000)
    # getWinRatio('THOMATO', 'fox')
    getAllWinRatios('THOMATO')
    #print(countAllWins('BEEF'))
