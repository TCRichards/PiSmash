import sqlite3
import os
import numpy as np
import datetime

from textRecognition.game import makeSampleGame

curDir = os.path.dirname('')
dataPath = os.path.join(curDir, 'gameLog.db')
conn = sqlite3.connect(dataPath)    # Stores the connection to the database


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


# ONLY EXECUTE THIS WHEN WE FIRST CREATE THE TABLE
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


# Returns all of the information stored about a given player
def searchPlayer(playerTag):
    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM games where player1 ='{}'".format(playerTag)) # Places Query result on the buffer
    cursor.execute('SELECT * FROM {}'.format(playerTag))
    return cursor.fetchall()    # Fetch the query result from the buffer


# Returns all information about every game played
def listGames():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM games')
    return cursor.fetchall()

# Fill in sample data
# cursor.execute("INSERT INTO games VALUES ('12-20-19.12:23:23', 'THOMATO', 'BEEF', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL')")
if __name__ == '__main__':
    game = makeSampleGame()
    logResults(game)

    # searchPlayer('THOMATO')
    print(listGames())
    conn.close()
