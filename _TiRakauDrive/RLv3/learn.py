from xml.dom import minidom
#import pandas as pd
import operator
import time
import numpy 

costs = minidom.parse("summary.xml")
stepCosts = []
meanWaitingTimes = []
steps = costs.getElementsByTagName('step') #vehicles halted 
for step in steps: 
    stepCosts.append(float(step.attributes['meanSpeed'].value)/int(step.attributes['running'].value)) #600 quantities of vehicles halting
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


stateActionValueTuple = [(states[step], actions[step], stepCosts[step]) for step in range(0, len(stepCosts))]

#stateActionValueTuple.append(['111111111111', -1, -1])
tupleNumber = 0
SARS = [] 
i = 0
while i < len(stateActionValueTuple)-1:
    rewardAverage = stateActionValueTuple[i][2]
    counter = 1
    # IMPORTANT check this again if state is changed
    # squash all the transition steps into 1 reward, if current phase is next step phase, action is next step action and action is not the same as state
    # stateActionValueTuple[i][0][1] = current phase, stateActionValueTuple[i+1][0][1] = next step phase
    # stateActionValueTuple[i][1] = action, stateActionValueTuple[i+1][1] = next step action
    
 
    if stateActionValueTuple[i][0][1] == stateActionValueTuple[i+1][0][1] and stateActionValueTuple[i][1] == stateActionValueTuple[i+1][1] and stateActionValueTuple[i][0][1] != stateActionValueTuple[i][1]:
        while i < len(stateActionValueTuple)-2 and stateActionValueTuple[i][0][1] == stateActionValueTuple[i+1][0][1] and stateActionValueTuple[i][1] == stateActionValueTuple[i+1][1] and stateActionValueTuple[i][0][1] != stateActionValueTuple[i][1]:
            i += 1
            counter += 1

            rewardAverage += stateActionValueTuple[i][2]


    i += 1
    # add State, action, reward, new state
    SARS.append([stateActionValueTuple[i-counter][0], stateActionValueTuple[i-counter][1], rewardAverage/float(counter), stateActionValueTuple[i][0] ])
SARS.pop()          #remove mid transition SARS 


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

SARS.append(['1111111111111', -1, -1, '1111111111111'])

stateActionValuesFile = open("stateActionValues.csv", "r")
stateActionValues = stateActionValuesFile.readlines()
stateActionValuesFile.close()
updatestateActionValues = open("stateActionValues.csv", "w")

        
learningRate = .04
gamma = 0.16 # discount factor
sARSNumber = 0 #points to number in list
maxGroup = 4 #TODO should not be hardcoded
rowNo = 0
delta = 0
for row in stateActionValues: #modifies the visited stateActions by finding the row and col of the stateActions
    rowValues = row.split(",",8)   
    currentState = SARS[sARSNumber][0]
    stateInDec = (int(currentState[0])*9*7) + (int(currentState[1])*9) + int(currentState[2],9) #convert the state to its row no equivalent
    if rowNo == stateInDec:                                             # if state has been observed in SARS list
        updatestateActionValues.write(str(rowValues[0] )+"," )          #don't forget to print the state
        i = 0
        while i < 7:  
            value = float(rowValues[i+1])                               # get the current value of the state/action pair
            if i == int(SARS[sARSNumber][1]) and rowNo == stateInDec:   # if action has been observed
                reward = SARS[sARSNumber][2]                       #value is -vehicles halting (we want to maximize the reward, hence minimize vehicle halting)
                nextStateValue = (SARS[sARSNumber][3])
                nextStateDec = (int(nextStateValue[0])*9*7) + (int(nextStateValue[1])*9) + int(nextStateValue[2],9)
                nextState = stateActionValues[nextStateDec]
                nextStateActions = [float(qValue) for qValue in nextState.split(",",8)[1:8]]
                maxAction = max(nextStateActions)
                update = value + (reward + (gamma*maxAction) - value)*learningRate                         #q-learning update, *maxAction by gamma?
                delta = delta + numpy.linalg.norm(update - value)   
                sARSNumber += 1
                currentState = SARS[sARSNumber][0]
                stateInDec = (int(currentState[0])*9*7) + (int(currentState[1])*9) + int(currentState[2],9)  #convert the state to its row no equivalent
    
                #if next SARS state and action is same as last, stay on the same, else increment 
                if int(SARS[sARSNumber][1]) != i or int(SARS[sARSNumber][0]) != int(SARS[sARSNumber-1][0]):
                    i += 1
                    updatestateActionValues.write(str(update )+",")

            
            else:
                updatestateActionValues.write(str(value)+",")
                i += 1
            
    else:                                                           #reprint what was read.        
        updatestateActionValues.write(str(rowValues[0] )+"," )
        for i in range(0,7):
            value = float(rowValues[i+1])                           # get the current value of the state/action pair
            updatestateActionValues.write(str(value)+",")
    updatestateActionValues.write("\n")
    rowNo += 1
           
learningUpdates = open("learningUpdates.csv", "a+")
learningUpdates.write(str(delta) + "\n")
learningUpdates.close()


     


    #stateActionValues = pd.read_csv("stateActionValues.csv", index_col=0)
    # cols are loop activations
    # rows are [activePhase][maxGroup]

    #print( list(stateActionValues['stateAction']).index(11)  ) # 10
    #row = list(stateActionValues['stateAction']).index(11)
    #col = '00000000'
    #stateActionValues.at[row, col] = 1
    #stateActionValues.to_csv('stateActionValues.csv')
    #print(stateActionValues['00000000'] )
    