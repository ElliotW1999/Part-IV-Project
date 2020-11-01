from xml.dom import minidom
import numpy

costs = minidom.parse("summary.xml")
stepCosts = []
meanWaitingTimes = []
steps = costs.getElementsByTagName('step') #vehicles halted 
meanSpeed = 0
for step in steps: 
    meanSpeed += float(step.attributes['meanSpeed'].value)
    
tripdata = open("tripinfoRL.xml", "r")
timeLoss = []
timeStopped = []
vehsProcessed = 0
for line in tripdata:
    line = line.split(' ')
    if len(line) > 4:
        if line[4] == "<tripinfo":
            timeLoss.append(float(line[20].split("\"")[1]))
            timeStopped.append(float(line[17].split("\"")[1]))
            vehsProcessed += 1
    
meanSpeed = meanSpeed/600
updateFile = open("meanSpeeds.csv", "a+")
updateFile.write( str(meanSpeed)+",")

updateFile.write(str(numpy.mean(timeLoss))+",")
updateFile.write(str(numpy.mean(timeStopped))+",")
updateFile.write(str(vehsProcessed)+",\n")
