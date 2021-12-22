#code adapted and modified from Psychphysics Laboratory Demos created by Dr. Adam Bricker
#@author: hilya

import pandas as pd
from statistics import mean

import matplotlib.pyplot as plt
import numpy as np

from statsmodels.stats.anova import AnovaRM


def extract_data(rawData):
    expData = pd.DataFrame (rawData, columns = ["block", "trial", "response", "stimFile", "key_resp_2.keys","key_resp_2.rt","participant"])
    expData = expData.rename(columns = {"response" : "condition", "key_resp_2.keys" : "resp","key_resp_2.rt" : "RT"})
    # deleting practice trials from dataframe - index values rows 0-16
    expData = expData.drop(labels=range(0,17), axis=0)
    #adding a block column
    expData["block"] = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,"end"]
    return (expData)        

#compiling individual files, reading and combining in one Database
#dataPath = "data_csv/"
#csvFiles = [dataPath + file for file in listdir(dataPath) if ".csv" in file]
#allData = pd.concat(map(pd.read_csv, csvFiles))      

##import data
dataPath = "data_group/"
dataFile = "002_psychophysicsHKA_2021_Dec_01_1411.csv"
rawData = pd.read_csv(dataPath + dataFile)

#retrieving relevant columns and deleting practice trials
expData = extract_data(rawData)

#getting only responded go trials
rtData = expData[expData.RT.notnull()]

##calculate mean RTs for each condition
#data frame for mean RTs
meanRTs = pd.DataFrame({"participant" : [], "mean RT" : []})

#lists for RTs for each condition i.e. stimulus intensity
min20db = []
min30db = []
min40db = []
min50db = []

#loop over data
for index, row in rtData.iterrows():
    #min20db is trials numbered 1
    if row["trial"] == 1:
        min20db.append(row["RT"])
    #min30db is trials numbered 2
    elif row["trial"] == 2:
       min30db.append(row["RT"])
    #min40db is trials numbered 3
    elif row["trial"] == 3:
        min40db.append(row["RT"])
    #min50db is trials numbered 4
    elif row["trial"] == 4:
        min50db.append(row["RT"])
        
#lists for RTs for each condition i.e. block
block1 = []
block2 = []
block3 = []
block4 = []
block5 = []
block6 = []
block7 = []
block8 = []

#loop over data
for index, row in rtData.iterrows():
    if row["block"] == 1:
        block1.append(row["RT"])
    elif row["block"] == 2:
        block2.append(row["RT"])
    elif row["block"] == 3:
        block3.append(row["RT"])
    elif row["block"] == 4:
        block4.append(row["RT"])
    elif row["block"] == 5:
        block5.append(row["RT"])
    elif row["block"] == 6:
        block6.append(row["RT"])
    elif row["block"] == 7:
        block7.append(row["RT"])
    elif row["block"] == 8:
        block8.append(row["RT"])

#new data to add to meanRTs
pNum = 2
pNumList1 = [pNum, pNum, pNum, pNum]
pNumList2 = [pNum, pNum, pNum, pNum, pNum, pNum, pNum, pNum]

intensityList = ["min20db", "min30db", "min40db", "min50db"]
blockList = ["block1", "block2", "block3", "block4", "block5", "block6", "block7", "block8"]

intensity_meanRTsList = [mean(min20db), mean(min30db), mean(min40db), mean(min50db)]
block_meanRTsList = [mean(block1), mean(block2), mean(block3), mean(block4), mean(block5), mean(block6), mean(block7), mean(block8)]

#new data --> data frame
newLines1 = pd.DataFrame({"participant" : pNumList1, "intensity" : intensityList,
                         "mean RT" : intensity_meanRTsList})
newLines2 = pd.DataFrame({"participant" : pNumList2, "block" : blockList, "mean RT" : block_meanRTsList})
#append newLines to meanRTs
#(note: unlike appending a list, this doesn't change the initial data frame)
intensity_meanRTs = meanRTs.append(newLines1, ignore_index=True)
block_meanRTs = meanRTs.append(newLines2, ignore_index=True)

#print (intensity_meanRTs)
#print (block_meanRTs)

"""
#plotting by intensity
fig, ax = plt.subplots()
box = ax.boxplot([min20db, min30db, min40db, min50db])
ax.set_ylabel("RT (s)")
ax.set_xticklabels(["min20db", "min30db", "min40db", "min50db"])
plt.show()

#plotting by block
fig, ax = plt.subplots()
box = ax.boxplot([block1, block2, block3, block4, block5, block6, block7, block8])
ax.set_ylabel("RT (s)")
ax.set_xticklabels(blockList)
plt.show()
"""
#statistics
model = AnovaRM(data = intensity_meanRTs and block_meanRTs, depvar = "mean RT", subject = "participant", within = ["intensity","block"]).fit()