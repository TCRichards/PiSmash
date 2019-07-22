from textRecognition import selectDetect as sd
from textRecognition import resultsDetect as rd


def makeGame():
    game = sd.loadImage(sd.imagePath)
    for player in game.players:
        player.printOut()
    rd.loadImage(rd.imagePath, game)
    for player in game.players:
        player.printOut()


makeGame()
