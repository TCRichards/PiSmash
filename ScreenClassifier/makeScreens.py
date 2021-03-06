'''
Uses character icons from Nintendo to generate a ton of training data
Authors: Thomas Richards and Nick Konz
Date Modified: 6/11/19
'''

import vlc
import pafy
import time
import os
import numpy as np

# Program that uses the VLC library to stream videos from YouTube
# Records screenshots and stores them in different directories depending on type
# IMPORTANT: After screenshots are recorded, go through directories and manually delete erroneous pictures

curDir = os.path.dirname(__file__)
trainingDir = os.path.join(curDir, 'trainingImages/')
validationDir = os.path.join(curDir, 'validationImages/')
testingDir = os.path.join(curDir, 'testingImages/')

winDir = os.path.join(trainingDir, 'Victory/')
gameDir = os.path.join(trainingDir, 'Game/')
selectDir = os.path.join(trainingDir, 'Select/')

num_rows, num_cols = 200, 200

directories = [winDir, gameDir, selectDir]

# Links to YouTube videos containing screenshots relevant to each category
winURL = 'https://www.youtube.com/watch?v=J0531h9USmI'
gameURL = ['https://www.youtube.com/watch?v=CyuRaYwb2XQ',
           'https://www.youtube.com/watch?v=TIV2PYIFkqE&t=33s',
           'https://www.youtube.com/watch?v=9nnZgn2v2r0',
           'https://www.youtube.com/watch?v=uuCcTgIRWeE',       # Included one 8-player game to spice things up
           'https://www.youtube.com/watch?v=rZsmUnhiQ5Q',
           'https://www.youtube.com/watch?v=5UuK89BaCSQ'
           ]

# This video only uses select screens with 2 players.  May need to add another
selectURLs = ['https://www.youtube.com/watch?v=KQvCBxsg_Z0',
              'https://www.youtube.com/watch?v=Tm577RyV-Fc'
              ]

# Make new directories if necessary
# for directory in directories:
#     try:
#         os.mkdir(directory)
#     except FileExistsError:
#         pass


# Helper function that instantiates a VLC media object using a Youtube video's URL
def setupPlayer(URL):
    video = pafy.new(URL)                   # Gets the URL where the video is actually hosted by YouTube
    best = video.getbest()                  # Gets the best quality video
    media = vlc.MediaPlayer(best.url)       # Link the media player to the YouTube video
    media.audio_set_mute(True)              # As much as I love hearing this 1000 times, mute it
    return media


# This is where the scanVideo method collects the parameters relevant to each type of video
def getParameters(type):
    prefix, dir = '', ''
    initialWait, wait = 0, 0
    if type == 'win':
        prefix = 'vicScreen_'
        dir = winDir
        initialWait = 14.4
        wait = 6.90
    elif type == 'game':
        dir = gameDir
        prefix = 'gameScreen_'
        initialWait = 0
        wait = 5
    elif type == 'select':
        initialWait = 15
        wait = 3
        dir = selectDir
        prefix = 'selectScreen_'
    return initialWait, wait, prefix, dir


# Function that plays the video for which a media object has already been created
# Captures screenshots throughout the video according to video's classification
def captureShots(type, media, trial, inputInitialWait=0, inputWait=0):
    initialWait, wait, prefix, dir = getParameters(type)
    if (inputInitialWait != 0):     # Handles if we want to manually enter a wait time (used by victory screen)
        initialWait = inputInitialWait
        wait = inputWait

    media.play()
    time.sleep(initialWait)

    counter = 0
    while(media.is_playing):    # Capture screenshots as long as the video is playing
        media.video_take_snapshot(0, dir + prefix + str(trial) + '_' + str(counter) + '.png', 0, 0)
        time.sleep(wait)        # Time until next screenshot
        counter += 1


# Called by original functions.  In charge of calling captureShots with spcecifics relating to
# classification of video type
def scanVideo(type, URL, trial):
    media = setupPlayer(URL)

    if type == 'win':
        for i in range(trial, trial + 10):                       # Repeat 10 times with slightly different timings to capture everything
            initialWait, wait = getParameters(type)[0], getParameters(type)[1]
            # Slightly change the wait time parameters and repeat
            initialWait = np.random.normal(initialWait, 0.01)
            steadyWait = np.random.normal(wait, 0.025)
            captureShots(type, media, i, inputInitialWait=initialWait, inputWait=steadyWait)
    else:           # For game or select screens
        captureShots(type, media, trial)


'''
I decided for the win screen that we should gather images of the beginning of the stats screen,
when the winning character is standing behind everyone's stats.  This seemed to me like the most uniform accross
characters, and would therefore be the best for classification.  This assumption may be incorrect, and if low performace
is achieved we should look at other possibilities, such as GAME! displayed at the end of a match, or the closeup of the winner
before the stats screen comes up.
'''


def makeWinScreens(trial):
    scanVideo('win', winURL, trial)


def makeGameScreens(index, trial):
    scanVideo('game', gameURL[index], trial)


def makeSelectScreens(index, trial):
    scanVideo('select', selectURLs[index], trial)


if __name__ == '__main__':
    # makeGameScreens(4, 4)
    # makeWinScreens(0)
    makeWinScreens(6)
    makeSelectScreens(1, 3)
