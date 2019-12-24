import sqlite3
import os
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
    count = getGameCount()
    cursor = conn.cursor()
    try:
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
        # conn.close()

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


def logGame(game):
    createGameTable()
    cursor = conn.cursor()
    command = """INSERT INTO games VALUES ('{}', '{}', {}, {})""".format(
    player.tag, now, player.charName, player.rank, 69)

    cursor.execute(command)
    conn.commit()


# Takes a player object as input and logs relevant information
def logPlayer(player):
    createPlayerTable(player.tag)   # Make sure that we have a table created for the player
    cursor = conn.cursor()
    now = datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
    command = """INSERT INTO {} VALUES ('{}', '{}', {}, {})""".format(
    player.tag, now, player.charName, player.rank, 69)

    cursor.execute(command)
    conn.commit()


def logResults(game):
    cursor = conn.cursor()
    cursor.execute('SELECT gameCount FROM master')
    numGames = cursor.fetchone()
    # Create for each player in the game, create a database table if we need to
    for player in game.players:
        logPlayer(player)
    logGame(game)
    conn.commit()


def searchPlayer(playerTag):
    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM games where player1 ='{}'".format(playerTag)) # Places Query result on the buffer
    cursor.execute('SELECT * FROM {}'.format(playerTag))
    return cursor.fetchall()    # Fetch the query result from the buffer


# Fill in sample data
# cursor.execute("INSERT INTO games VALUES ('12-20-19.12:23:23', 'THOMATO', 'BEEF', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL')")
if __name__ == '__main__':
    # game = makeSampleGame()
    # logResults(game)
    # searchPlayer('THOMATO')


    createMasterTable(reset=False)
    print(getGameCount())
    incrementGameCount()
    print(getGameCount())

    conn.close()
