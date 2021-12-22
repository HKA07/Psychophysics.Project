#@author: hilya
#code adapted and modified from Psychphysics Laboratory Demos created by Dr. Adam Bricker

import pandas as pd
import matplotlib.pyplot as plt

from statistics import mean
from os import listdir

#function deleting practice trials, and filtering responded 'go' trials
def extract_data(rawData):
    expData = pd.DataFrame (rawData, columns = ["block", "trial", "response", "stimFile", "slider_2.response", "key_resp_2.keys","participant"])
    expData = expData.rename(columns = {"response" : "task", "key_resp_2.keys" : "resp", "slider_2.response" : "rating"})
    # deleting practice trials from dataframe - index values rows 0-16
    expData = expData.drop(labels=range(0,17), axis=0)
    #adding a block column
    expData["block"] = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,"end"]
    return (expData)

#creating filepath
dataPath = "data_csv/"
fileList = listdir(dataPath)

#creating new dataframe for meanRTs
intensity_meanRTs = pd.DataFrame({"participant" : [], "mean RT" : []})
block_meanRTs = pd.DataFrame({"participant" : [], "mean RT" : []})
#data frame for mean RTs
meanRTs = pd.DataFrame({"participant" : [], "mean RT" : []})

counter = 0
for dataFile in fileList:
    #New ID for each participant
    counter += 1
    pNum = "P-" + str(counter)
    rawData = pd.read_csv(dataPath + dataFile)
    #only include relevant columns, exclude practice trials
    expData = extract_data(rawData)

    #SDT measures dataframe
    rating = pd.DataFrame({"condition" : ["noSound", "min20db", "min30db", "min40db", "min50db"],"hits" : [0,0,0,0,0], "misses" : [0,0,0,0,0], "CRs" : [0,0,0,0,0], "FAs" : [0,0,0,0,0]})

    for index, row in expData.iterrows():
        #condition: no sound
        rowInd = 0
        #Hit
        if row["task"] == "nogo" and row["rating"] == 0:
            rating.loc[rowInd,"hits"] += 1
        #Miss
        elif row["task"] == "nogo" and row["rating"] != 0:
            rating.loc[rowInd,"misses"] += 1
        #Correct rejection
        elif row["task"] == "go" and row["rating"] != 0:
            rating.loc[rowInd,"CRs"] += 1
        #False alarm
        elif row["task"] == "go" and row["rating"] == 0:
            rating.loc[rowInd,"FAs"] += 1
        
        #condition: min20db
        rowInd = 1
        #Hit
        if row["task"] == "go" and row["trial"] == 1 and row["rating"] == 1:
            rating.loc[rowInd,"hits"] += 1
        #Miss
        elif row["task"] == "go" and row["trial"] == 1 and row["rating"] != 1:
            rating.loc[rowInd,"misses"] += 1
        #Correct rejection
        elif row["task"] == "nogo" and row["rating"] == 0:
            rating.loc[rowInd,"CRs"] += 1
        #False alarm
        elif row["task"] == "nogo" and row["rating"] == 1:
            rating.loc[rowInd,"FAs"] += 1
        
        #condition: min30db
        rowInd = 2
        #Hit
        if row["trial"] == 2 and row["rating"] == 2:
            rating.loc[rowInd,"hits"] += 1
        #Miss
        elif row["trial"] == 2 and row["rating"] != 2:
            rating.loc[rowInd,"misses"] += 1
        #Correct rejection
        elif row["task"] == "nogo" and row["rating"] == 0:
            rating.loc[rowInd,"CRs"] += 1
        #False alarm
        elif row["task"] == "nogo" and row["rating"] == 2:
            rating.loc[rowInd,"FAs"] += 1
        
        #condition: min40db
        rowInd = 3
        #Hit
        if row["trial"] == 3 and row["rating"] == 3:
            rating.loc[rowInd,"hits"] += 1
        #Miss
        elif row["trial"] == 3 and row["rating"] != 3:
            rating.loc[rowInd,"misses"] += 1
        #Correct rejection
        elif row["task"] == "nogo" and row["rating"] == 0:
            rating.loc[rowInd,"CRs"] += 1
        #False alarm
        elif row["task"] == "nogo" and row["rating"] == 3:
            rating.loc[rowInd,"FAs"] += 1
        
        #condition: min50db
        rowInd = 4
        #Hit
        if row["trial"] == 4 and row["rating"] == 1:
            rating.loc[rowInd,"hits"] += 1
        #Miss
        elif row["trial"] == 4 and row["rating"] != 1:
            rating.loc[rowInd,"misses"] += 1
        #Correct rejection
        elif row["task"] == "nogo" and row["rating"] == 0:
            rating.loc[rowInd,"CRs"] += 1
        #False alarm
        elif row["task"] == "nogo" and row["rating"] == 4:
            rating.loc[rowInd,"FAs"] += 1
        
    print (pNum)
    print (rating)