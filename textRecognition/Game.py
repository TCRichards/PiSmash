class Game:

    def __init__(self, players):
        self.players = players

    def printOut(self):
        for player in self.players:
            player.printOut()


# Make a sample game object for testing and debugging
def makeSampleGame():
    import os
    import sys
    from inspect import getsourcefile

    current_path = os.path.abspath(getsourcefile(lambda: 0))
    current_dir = os.path.dirname(current_path)
    parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
    sys.path.insert(0, parent_dir)

    import numpy as np
    from .player import Player      # Class wrapping a Player's character, tag, and rank
    from IconClassifier.iconModel import charDict

    chars = list(charDict.keys())   # Get the names of all the characters
    p1 = Player('THOMATO', chars[np.random.randint(len(chars))], 1, 1)  # Me vs. Nick with random characters
    p2 = Player('BEEF', chars[np.random.randint(len(chars))], 2, 2)
    sampleGame = Game([p1, p2]) # Make the sample game object and return it
    return sampleGame

if __name__ == '__main__':
    makeSampleGame()
