from xml.dom import minidom

costs = minidom.parse("summary.xml")
stepCosts = []
meanWaitingTimes = []
steps = costs.getElementsByTagName('step') #vehicles halted 
meanSpeed = 0
for step in steps: 
    meanSpeed += float(step.attributes['meanSpeed'].value)
    
meanSpeed = meanSpeed/600
updateFile = open("meanSpeeds.csv", "a+")
updateFile.write( str(meanSpeed)+"\n")