import matplotlib.pyplot as plt
import numpy
from xml.dom import minidom

tripdata = minidom.parse("output/tripinfoEDF.xml")
timeLoss = []
timeStopped = []
trips = tripdata.getElementsByTagName('tripinfo') #vehicles trips 
for trip in trips:
    timeLoss.append(float(trip.attributes['timeLoss'].value))
    timeStopped.append(float(trip.attributes['waitingTime'].value))
            
            
binsvalues = []
binsvalues.append(0)
#binsvalues.append(1)
for i in range(1,51):
    binsvalues.append(int(max(timeLoss)*i/50))
    
plt.title('Time at suboptimal speed')
plt.xlabel('Time loss (s)')
plt.ylabel('Number of vehs')
plt.hist(timeLoss, bins=binsvalues)
plt.show()

binsvalues = []
binsvalues.append(0)
#binsvalues.append(1)
for i in range(1,51):
    binsvalues.append(int(max(timeStopped)*i/50))
    
plt.title('Time stopped')
plt.xlabel('Time (s)')
plt.ylabel('Number of vehs')
plt.hist(timeLoss, bins=binsvalues)
plt.show()

print(numpy.mean(timeLoss))
print(numpy.std(timeLoss))

print(numpy.mean(timeStopped))
print(numpy.std(timeStopped))
print(len(timeLoss))

from xml.dom import minidom

costs = minidom.parse("output/summary.xml")
stepCosts = []
meanWaitingTimes = []
steps = costs.getElementsByTagName('step') #vehicles halted 
for step in steps: 
    stepCosts.append(float(step.attributes['meanSpeed'].value)) #600 quantities of vehicles halting
    
print(str(sum(stepCosts)/600))
