class Player:

    def __init__(self, tag, charName, playerNum, rank):
        self.tag = tag
        self.charName = charName
        self.playerNum = playerNum
        self.rank = rank

    # Conviniently print out all data
    def printOut(self):
        print('Character Name = ' + self.charName)
        print('Player Tag = ' + self.tag)
        print('Player Number = ' + str(self.playerNum))
        print('Current Rank = ' + str(self.rank))
