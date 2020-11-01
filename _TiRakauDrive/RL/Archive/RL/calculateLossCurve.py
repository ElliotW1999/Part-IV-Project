from xml.dom import minidom

costs = minidom.parse("summary.xml")
stepCosts = []
meanWaitingTimes = []
steps = costs.getElementsByTagName('step') #vehicles halted 
for step in steps: 
    stepCosts.append(int(step.attributes['halting'].value)) #600 quantities of vehicles halting
    meanWaitingTimes.append(float(step.attributes['meanWaitingTime'].value)) # for loss curves
    
    
lossCurve = open("generateLossCurves.csv", "a+")
lossCurve.write( str(sum(stepCosts)))
lossCurve.write( " ")
lossCurve.write( str(sum(meanWaitingTimes)))
lossCurve.write( "\n")
lossCurve.close()
