class Game:

    def __init__(self, players):
        self.players = players

    def printOut(self):
        for player in self.players:
            player.printOut()


# Make a sample game object for testing and debugging
def makeSampleGame(numPlayers):
    import os
    import sys
    from inspect import getsourcefile
    from random import shuffle

    current_path = os.path.abspath(getsourcefile(lambda: 0))
    current_dir = os.path.dirname(current_path)
    parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
    sys.path.insert(0, parent_dir)

    import numpy as np
    try:
        from .player import Player      # Class wrapping a Player's character, tag, and rank
    except ModuleNotFoundError:
        from player import Player
    from IconClassifier.iconModel import charDict

    # Create the data entries
    playerNames = ['THOMATO', 'BEEF', 'gottapoot', 'protosnipe', 'gary-san', 'LIGMA', 'BIRD', 'QLIVER']
    ranks = np.arange(1, numPlayers + 1)
    orders = np.arange(1, numPlayers + 1)

    # And randomize everything for fun
    # shuffle(playerNames) # Don't shuffle player names for now so we can gather sufficient data for a small number
    shuffle(ranks)
    shuffle(orders)

    chars = list(charDict.keys())   # Get the names of all the characters
    players = []
    for i in range(numPlayers):     # Create the desired number of radomized characters
        players.append(Player(playerNames[i], chars[np.random.randint(len(chars))], ranks[i], orders[i]))
    sampleGame = Game(players) # Make the sample game object and return it
    return sampleGame


if __name__ == '__main__':
    makeSampleGame(3).printOut()
