import sqlite3
import os
import datetime

from textRecognition.game import makeSampleGame

curDir = os.path.dirname('')
dataPath = os.path.join(curDir, 'gameLog.db')
conn = sqlite3.connect(dataPath)    # Stores the connection to the database

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
    except sqlite3.OperationalError:
        print('Table Already Exists')
    finally:
        conn.commit()
        # conn.close()

# Creates a table for the given player tag that stores data from each game
def createPlayerTable(playerName):
    cursor = conn.cursor()
    try:
        # Create the object
        cursor.execute("""CREATE TABLE {} (
                        timestamp TEXT,
                        charName TEXT,
                        rank INTEGER,
                        damage INTEGER
                        )""".format(playerName))
    except sqlite3.OperationalError:
        print('Table Already Exists')
    finally:
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


def logGame(game):
    cursor = conn.cursor()
    game.printOut()
    # Create for each player in the game, create a database table if we need to
    for player in game.players:
        logPlayer(player)
    conn.commit()


def searchPlayer(playerTag):
    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM games where player1 ='{}'".format(playerTag)) # Places Query result on the buffer
    cursor.execute('SELECT * FROM {}'.format(playerTag))
    gameList = cursor.fetchall()    # Fetch the query result from the buffer
    print(gameList)                 # Prints out all the games where the statement is true
    conn.commit()

# Fill in sample data
# cursor.execute("INSERT INTO games VALUES ('12-20-19.12:23:23', 'THOMATO', 'BEEF', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL')")
if __name__ == '__main__':
    game = makeSampleGame()
    logGame(game)
    searchPlayer('THOMATO')
    conn.close()

    # createTable()
    # searchPlayer('THOMATO')
