import PIL
from PIL import Image, ImageOps, ImageEnhance, ImageDraw
import pyautogui as pg
import pandas as pd
import numpy as np
import easyocr


"""

This script was used more as a proof of concept for the project.
To see a full breakdown of the code go to the Stat-Tracker.pdf file 

"""



def imagePrep(path):
    
    #Take image and crop into a vertical row of pixels on the left of the scoreboard
    imgOriginal = Image.open(path)
    # imgOriginal.show()

    imgFindPlayer = imgOriginal.crop((330,330,331,800))

    #Convert string of pixels into an array and find the top and bottom white pixels
    na = np.array(imgFindPlayer)
    Y,X= np.where(np.all(na==[255,255,255],axis=2))
    top, bottom = Y[0], Y[-1]

    #Crop original image to just the player's row
    imgNums = imgOriginal.crop((600,330+top,1450,bottom+330))
    imgNums.save(r'C:\Users\Hollis\Desktop\scoreboardcropped.png')
    # imgNums.show()

    #Crop image for column names
    imgCols = imgOriginal.crop((760,330,1450,380))
    imgCols.save(r'C:\Users\Hollis\Desktop\scoreboardcroppedcolumns.png')
    # imgCols.show()

    reader = easyocr.Reader(['en'])
    playerResult = reader.readtext(r'C:\Users\Hollis\Desktop\scoreboardcropped.png', detail = 0, text_threshold= .5, low_text=.001)
    playerResult = playerResult[0].split()
    playerResult = [int(i) for i in playerResult]
    print(playerResult)
    columnsResult = reader.readtext(r'C:\Users\Hollis\Desktop\scoreboardcroppedcolumns.png', detail = 0, text_threshold= .9, low_text=.3)
    columnsResult = [i.strip() for i in columnsResult if i.strip().isalpha()]
    print(columnsResult)

    statColumns = ['DATE', 'SCORE', 'KILLS', 'DEATHS', 'CONFIRMS', 'DENIES', 'TIME', 'ASSISTS', 'LATENCY', 'PLANTS', 'DEFUSES']

    masterData = pd.read_csv(r'C:\Users\Hollis\Documents\CodStats\stats.csv')

    statsData = pd.DataFrame(columns=columnsResult)
    statsData.loc[len(statsData)+1] = playerResult
    # statsData.head()
    # masterData = pd.DataFrame()
    masterData = pd.concat([statsData, masterData], axis=0, ignore_index=True)

    k = int(masterData['KILLS'].sum())
    d = int(masterData['DEATHS'].sum())
    kd = k/d
    print(f'KD: {kd}')
    avgScore = masterData['SCORE'].mean()
    print(f'Average Score: {avgScore}')

    masterData.to_csv(r'C:\Users\Hollis\Documents\CodStats\stats.csv', index=False)

    print(masterData)

imagePrep(r'C:\Users\Hollis\Desktop\scoreboard4.png')

