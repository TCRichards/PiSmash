class Player:

    # Initialize a player object
    def __init__(self, tag, charName, playerNum, rank=None):
        self.tag = tag                      # Username. e.g. 'THOMATO'
        self.charName = charName            # Name of the charcter being played
        self.playerNum = playerNum          # Player number assignment. e.g. 'P1'
        self.rank = rank                    # How did the player do?  This will be None until assigned at the end

    # Conviniently print out all data fields
    def printOut(self):
        print('Character Name = ' + self.charName)
        print('Player Tag = ' + self.tag)
        print('Player Number = ' + str(object=self.playerNum))
        print('Current Rank = ' + str(self.rank))


if __name__ == '__main__':
    pass
