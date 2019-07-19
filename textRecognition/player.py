class Player:

    def __init__(self, tag, charName, rank):
        self.tag = tag
        self.charName = charName
        self.rank = rank

    def __init__(self, tag, charName):
        self.tag = tag
        self.charName = charName
        self.rank = -1  # If we don't yet know the rank (as in from select screen), set it to -1

    # Conviniently print out all data
    def printOut(self):
        print('Character Name = ' + self.charName)
        print('Player Tag = ' + self.tag)
        print('Current Rank = ' + str(rank))
