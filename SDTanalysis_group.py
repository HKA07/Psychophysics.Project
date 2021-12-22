#@author: hilya
#code adapted and modified from Psychphysics Laboratory Demos created by Dr. Adam Bricker

import pandas as pd
from scipy.stats import norm
from os import listdir

def extract_data(rawData):
    expData = pd.DataFrame (rawData, columns = ["block", "trial", "response", "stimFile", "key_resp_2.keys","key_resp_2.rt","participant"])
    expData = expData.rename(columns = {"response" : "task", "key_resp_2.keys" : "resp","key_resp_2.rt" : "RT"})
    # deleting practice trials from dataframe - index values rows 0-16
    expData = expData.drop(labels=range(0,17), axis=0)
    #adding a block column
    expData["block"] = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,"end"]
    return (expData)  

        
#d' function
def dPrime(hitRate, FArate):
    stat = norm.ppf(hitRate) - norm.ppf(FArate)
    return stat
#criterion function
def criterion(hitRate, FArate):
    stat = -.5*(norm.ppf(hitRate) + norm.ppf(FArate))
    return stat      

#import data
#creating filepath
dataPath = "data_csv/"
fileList = listdir(dataPath)

#for group d' and criterion
dPrimeList = []
criterionList = []

counter = 0
for dataFile in fileList:
    #New ID for each participant
    counter += 1
    pNum = "P-" + str(counter)
    rawData = pd.read_csv(dataPath + dataFile)
    print (dataPath + dataFile)
    #only include relevant columns, exclude practice trials
    expData = extract_data(rawData)

    #SDT measures dataframe
    accuracy = pd.DataFrame({"condition" : ["sound"],"hits" : [0], "misses" : [0,], "CRs" : [0], "FAs" : [0]})

    for index, row in expData.iterrows():
        rowInd = 0
        #Hit
        if row["task"] == "go" and row["resp"] == "space":
            accuracy.loc[rowInd,"hits"] += 1
        #Miss
        elif row["task"] == "go" and row["resp"] == "None":
            accuracy.loc[rowInd,"misses"] += 1
        #Correct rejection
        elif row["task"] == "nogo" and row["resp"] == "None":
            accuracy.loc[rowInd,"CRs"] += 1
        #False alarm
        elif row["task"] == "nogo" and row["resp"] == "space":
            accuracy.loc[rowInd,"FAs"] += 1
    
    print (pNum)
    print (accuracy)
    
    #calculating hit and false alarm rates
    
    hitRate = (accuracy.loc[0,"hits"])/32
    FArate = (accuracy.loc[0,"FAs"])/32
    
    if (accuracy.loc[0,"FAs"]) == 0:
        FArate = (accuracy.loc[0,"FAs"]+1)/32
    else: 
        pass
    
    if (accuracy.loc[0,"FAs"]) == 0 and (accuracy.loc[0,"hits"]) == 32:
        hitRate = 31
        FArate = (accuracy.loc[0,"FAs"]+1)/32
    else:
        pass
    
    print ("hit rate:", hitRate)
    print ("FA rate:", FArate)
    
    dprime = dPrime(hitRate,FArate)
    print ("d':", dprime)
    
    Criterion = criterion(hitRate,FArate)
    print ("criterion:", Criterion)
    
    if dprime is int or float:
        dPrimeList.append(dprime)
    else:
        pass
    
    if Criterion is int or float:
        criterionList.append(Criterion)
    #end of loop
    
avg_dprime = sum(dPrimeList)/len(dPrimeList)
avg_criterion = sum(criterionList)/len(criterionList)

print ("group d':", avg_dprime)
print ("group criterion:", avg_criterion)