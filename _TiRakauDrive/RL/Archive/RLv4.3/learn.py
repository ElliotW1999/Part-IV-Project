from xml.dom import minidom
#import pandas as pd
import operator
import time
import numpy 
import sqlite3
import os
from sqlite3 import Error
costs = minidom.parse("summary.xml")
stepCosts = []
meanWaitingTimes = []
steps = costs.getElementsByTagName('step') #vehicles halted 
for step in steps: 
    stepCosts.append(float(step.attributes['meanSpeed'].value)) #600 quantities of vehicles halting
    meanWaitingTimes.append(float(step.attributes['meanTravelTime'].value)) # for loss curves, TODO remove
    
    
stateActionsFile = open("stateActions.csv", "r")

states = []
actions = []
for stateAction in stateActionsFile: # loops active, newLight (optional)
    stateAction = stateAction.split(",")                  
    stateAction[-1] = stateAction[-1].replace('\n','')
    states.append(stateAction[0])
    actions.append(stateAction[1])
    
stateActionsFile.close()
stateActionValueTuple = [(states[step], actions[step], stepCosts[step]) for step in range(60, len(stepCosts))]


tupleNumber = 0
SARS = [] 
i = 0
while i < len(stateActionValueTuple)-1:
    rewardAverage = stateActionValueTuple[i][2]
    counter = 1
    # IMPORTANT check this again if state is changed
    # squash all the transition steps into 1 reward, if current phase is next step phase, action is next step action and action is not the same as state
    # stateActionValueTuple[i][0][2] = current phase, stateActionValueTuple[i+1][0][2] = next step phase
    # stateActionValueTuple[i][1] = action, stateActionValueTuple[i+1][1] = next step action
    
 
    if stateActionValueTuple[i][0][2] == stateActionValueTuple[i+1][0][2] and stateActionValueTuple[i][1] == stateActionValueTuple[i+1][1] and stateActionValueTuple[i][0][2] != stateActionValueTuple[i][1]:
        while i < len(stateActionValueTuple)-2 and stateActionValueTuple[i][0][2] == stateActionValueTuple[i+1][0][2] and stateActionValueTuple[i][1] == stateActionValueTuple[i+1][1] and stateActionValueTuple[i][0][2] != stateActionValueTuple[i][1]:
            i += 1
            counter += 1
            rewardAverage += stateActionValueTuple[i][2]
    i += 1
    # add State, action, reward, new state
    SARS.append([stateActionValueTuple[i-counter][0], stateActionValueTuple[i-counter][1], rewardAverage/float(counter), stateActionValueTuple[i][0] ])    
SARS.pop()          #remove mid transition SARS 
SARS.pop(0)    
SARS = (sorted(SARS, key=operator.itemgetter(0,1,3)))

#get all the repeat SARS    
SARSsimplified = []
i = 0
while i < len(SARS):
    SARSfiltered = [bar for bar in SARS if bar[0] == SARS[i][0] and bar[1] == SARS[i][1] and bar[3] == SARS[i][3]]
    noOfSARS = len(SARSfiltered)
    avgCost = sum(bar[2] for bar in SARSfiltered)/ noOfSARS          
    SARSsimplified.append([SARSfiltered[0][0], SARSfiltered[0][1], avgCost, SARSfiltered[0][3]])
    i += noOfSARS
SARS = SARSsimplified

# make this a function
db_file = os.getcwd()+"\QTable.db"
conn = None
try:
    conn = sqlite3.connect(db_file)
except Error as e:
    print(e)
cur = conn.cursor()
        
learningRate = .01
gamma = 0.32 # discount factor
sARSNumber = 0 #points to number in list
maxGroup = 4 #TODO should not be hardcoded
rowNo = 0
delta = 0

for transition in SARS:
    currentState = transition[0]
    stateInDec = (int(currentState[0])*9*10*9*7) + (int(currentState[1])*10*9*7) + (int(currentState[2])*9*7) + (int(currentState[3])*9) + int(currentState[4],9)+1  #convert the state to its row no equivalent
    cur.execute("SELECT Move"+str(int(transition[1])+1)+" FROM States WHERE rowid = " +str(stateInDec) )
    value = cur.fetchone()[0]
    reward = transition[2]
    
    nextStateValue = transition[3]
    nextStateDec = (int(nextStateValue[0])*9*10*9*7) + (int(nextStateValue[1])*10*9*7) + (int(nextStateValue[2])*9*7) + (int(nextStateValue[3])*9) + int(nextStateValue[4],9)+1  #convert the state to its row no equivalent
    cur.execute("SELECT * FROM States WHERE rowid = " +str(nextStateDec) )
    nextStateActions = cur.fetchone()
    maxAction = max(nextStateActions)
    
    update = value + (reward + (gamma*maxAction) - value)*learningRate                         #q-learning update, *maxAction by gamma?
    delta = delta + numpy.linalg.norm(reward + (gamma*maxAction) - value)   
    
    cur.execute("UPDATE States SET Move" +str(int(transition[1])+1)+ "= " +str(update)+ " WHERE rowid = " +str(stateInDec)) 
conn.commit()

learningUpdates = open("learningUpdates.csv", "a+")
learningUpdates.write(str(delta) + "\n")
learningUpdates.close()

        