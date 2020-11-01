from xml.dom import minidom

costs = minidom.parse("summary.xml")
stepCosts = []
meanWaitingTimes = []
steps = costs.getElementsByTagName('step') #vehicles halted 
for step in steps: 
    stepCosts.append(float(step.attributes['meanSpeed'].value)) #600 quantities of vehicles halting
    meanWaitingTimes.append(float(step.attributes['meanWaitingTime'].value)) # for loss curves
    
tripdata = open("tripinfoRL.xml", "r")
timeLoss = 0
for line in tripdata:
    line = line.split(' ')
    if len(line) > 4:
        if line[4] == "<tripinfo":
            timeLoss += 1
    
    
lossCurve = open("generateLossCurves.csv", "a+")
lossCurve.write( str(sum(stepCosts)))
lossCurve.write( " ")
lossCurve.write( str(timeLoss))
lossCurve.write( "\n")
lossCurve.close()
