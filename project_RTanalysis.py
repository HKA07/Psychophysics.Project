#@author: hilya
#code adapted and modified from Psychphysics Laboratory Demos created by Dr. Adam Bricker

import pandas as pd
import matplotlib.pyplot as plt

from statistics import mean
from os import listdir
from statsmodels.stats.anova import AnovaRM

#function deleting practice trials, and filtering responded 'go' trials
def extract_data(rawData):
    expData = pd.DataFrame (rawData, columns = ["block", "trial", "response", "stimFile", "key_resp_2.keys","key_resp_2.rt","participant"])
    expData = expData.rename(columns = {"response" : "task", "key_resp_2.keys" : "resp","key_resp_2.rt" : "RT"})
    # deleting practice trials from dataframe - index values rows 0-16
    expData = expData.drop(labels=range(0,17), axis=0)
    #adding a block column
    expData["block"] = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,"end"]
    return (expData)

#credit to Claudia Tato
def remove_outliers(df_in, col_name):
       q1 = df_in[col_name].quantile(0.25)
       q3 = df_in[col_name].quantile(0.75)
       iqr = q3 - q1 #Interquartile range
       fence_low = q1 - 1.5 * iqr
       fence_high = q3 + 1.5 * iqr
       df_out = df_in.loc[(df_in[col_name] > fence_low) & (df_in[col_name] < fence_high)]
       return df_out

#creating filepath
dataPath = "data_csv/"
fileList = listdir(dataPath)

#creating new dataframe for meanRTs
intensity_meanRTs = pd.DataFrame({"participant" : [], "mean RT" : []})
block_meanRTs = pd.DataFrame({"participant" : [], "mean RT" : []})
#data frame for mean RTs
meanRTs = pd.DataFrame({"participant" : [], "mean RT" : []})

counter = 0
#looping over each participant data file
for dataFile in fileList:
    #New ID for each participant
    counter += 1
    pNum = "P-" + str(counter)
    #print (dataPath+dataFile)
    rawData = pd.read_csv(dataPath + dataFile)
    #only include relevant columns, exclude practice trials
    expData = extract_data(rawData)
    #getting only responded go trials
    rtData = expData[(expData.task == "go") & (expData.resp == "space")] 
    #print (rtData)
    rtData = remove_outliers(rtData, "RT")
    
    #data frame for RTs for each condition (intensity type)
    min20dbRTs = rtData[(rtData.stimFile == "piano_min20db.wav")].RT
    min30dbRTs = rtData[(rtData.stimFile == "piano_min30db.wav")].RT
    min40dbRTs = rtData[(rtData.stimFile == "piano_min40db.wav")].RT
    min50dbRTs = rtData[(rtData.stimFile == "piano_min50db.wav")].RT
    
    #data frame for RTs for each condition (block)
    block1RTs = rtData[(rtData.block == 1)].RT
    block2RTs = rtData[(rtData.block == 2)].RT
    block3RTs = rtData[(rtData.block == 3)].RT
    block4RTs = rtData[(rtData.block == 4)].RT
    block5RTs = rtData[(rtData.block == 5)].RT
    block6RTs = rtData[(rtData.block == 6)].RT
    block7RTs = rtData[(rtData.block == 7)].RT
    block8RTs = rtData[(rtData.block == 8)].RT
    
    #new entries to add to meanRTs dataframe, seperate for each condition type
    pNumList1 = [pNum, pNum, pNum, pNum]
    pNumList2 = [pNum, pNum, pNum, pNum, pNum, pNum, pNum, pNum]
    
    #entries for condition
    intensityList = ["min20db", "min30db", "min40db", "min50db"]
    blockList = [1,2,3,4,5,6,7,8]

    #filling in intensity_meanRTsList with meanRTs based on intensity, and 0 if empty    
    intensity_meanRTsList = []
    if len (min20dbRTs) > 0:
        intensity_meanRTsList.append(mean(min20dbRTs))
    else:
        intensity_meanRTsList.append(0)
    if len (min30dbRTs) > 0:
        intensity_meanRTsList.append(mean(min30dbRTs))
    else:
        intensity_meanRTsList.append(0)
    if len (min40dbRTs) > 0:
        intensity_meanRTsList.append(mean(min40dbRTs))
    else:
        intensity_meanRTsList.append(0)
    if len (min50dbRTs) > 0:
        intensity_meanRTsList.append(mean(min50dbRTs))
    else:
        intensity_meanRTsList.append(0)
        
    #filling in block_meanRTsList with meanRTs of blocks, and 0 if block is empty
    block_meanRTsList = []
    if len (block1RTs) > 0:
        block_meanRTsList.append(mean(block1RTs))
    else:
        block_meanRTsList.append(0)
    if len (block2RTs) > 0:
        block_meanRTsList.append(mean(block2RTs))
    else:
        block_meanRTsList.append(0)
    if len (block3RTs) > 0:
        block_meanRTsList.append(mean(block3RTs))
    else:
        block_meanRTsList.append(0)
    if len (block4RTs) > 0:
        block_meanRTsList.append(mean(block4RTs))
    else:
        block_meanRTsList.append(0)
    if len (block5RTs) > 0:
        block_meanRTsList.append(mean(block5RTs))
    else:
        block_meanRTsList.append(0)
    if len (block6RTs) > 0:
        block_meanRTsList.append(mean(block6RTs))
    else:
        block_meanRTsList.append(0)
    if len (block7RTs) > 0:
        block_meanRTsList.append(mean(block7RTs))
    else:
        block_meanRTsList.append(0)
    if len (block8RTs) > 0:
        block_meanRTsList.append(mean(block8RTs))
    else:
        block_meanRTsList.append(0)
    

    #new data --> data frame
    newLines1 = pd.DataFrame({"participant" : pNumList1, "intensity" : intensityList,
                             "mean RT" : intensity_meanRTsList})
    newLines2 = pd.DataFrame({"participant" : pNumList2, "block" : blockList, "mean RT" : block_meanRTsList})
    #append newLines to meanRTs
    #(note: unlike appending a list, this doesn't change the initial data frame)
    intensity_meanRTs = intensity_meanRTs.append(newLines1, ignore_index=True)
    block_meanRTs = block_meanRTs.append(newLines2, ignore_index=True)
    #end of loop  

#plotting

#dataframe of meanRTs for each condition
min20db = intensity_meanRTs[(intensity_meanRTs.intensity == "min20db")] ["mean RT"]
min30db = intensity_meanRTs[(intensity_meanRTs.intensity == "min30db")] ["mean RT"]
min40db = intensity_meanRTs[(intensity_meanRTs.intensity == "min40db")] ["mean RT"]
min50db = intensity_meanRTs[(intensity_meanRTs.intensity == "min50db")] ["mean RT"]

#intensity plotting
fig, ax = plt.subplots()
box = ax.boxplot([min20db, min30db, min40db, min50db])
ax.set_ylabel("RT (s)")
ax.set_xticklabels(["min20db", "min30db", "min40db", "min50db"])
plt.show()

#intensity plotting
fig, ax = plt.subplots()
box = ax.boxplot([min20db, min30db, min40db, min50db])
ax.set_ylabel("RT (s)")
ax.set_xticklabels(["min20db", "min30db", "min40db", "min50db"])
plt.show()

#data frame for RTs for each condition (block)
block1 = block_meanRTs[(block_meanRTs.block == 1)] ["mean RT"]
block2 = block_meanRTs[(block_meanRTs.block == 2)] ["mean RT"]
block3 = block_meanRTs[(block_meanRTs.block == 3)] ["mean RT"]
block4 = block_meanRTs[(block_meanRTs.block == 4)] ["mean RT"]
block5 = block_meanRTs[(block_meanRTs.block == 5)] ["mean RT"]
block6 = block_meanRTs[(block_meanRTs.block == 6)] ["mean RT"]
block7 = block_meanRTs[(block_meanRTs.block == 7)] ["mean RT"]
block8 = block_meanRTs[(block_meanRTs.block == 8)] ["mean RT"]

#block plotting
fig, ax = plt.subplots()
box = ax.boxplot([block1, block2, block3, block4, block5, block6, block7, block8])
ax.set_ylabel("RT (s)")
ax.set_xticklabels(["block 1", "block 2", "block 3", "block 4", "block 5", "block 6", "block 7", "block 8"])
plt.show()

#statistics
model = AnovaRM(data = intensity_meanRTs, depvar = "mean RT", subject = "participant", within = ["intensity"]).fit()
model2 = AnovaRM(data = block_meanRTs, depvar = "mean RT", subject = "participant", within = ["block"]).fit()
print (model)
print (model2)
