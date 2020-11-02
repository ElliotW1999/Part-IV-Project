import matplotlib.pyplot as plt
import numpy 

lossCurves = open("generateLossCurves.csv", "r")
vehiclesProcessed = []
meanSpeeds = []

i = 0
for line in lossCurves:
    line = line.split(" ")
    if (i < 3000):
        vehiclesProcessed.append(float(line[2])/600)
        meanSpeeds.append(float(line[0])/600)
        
    i += 1



plt.scatter(vehiclesProcessed, meanSpeeds)
plt.title('Reward per episode')
plt.xlabel('vehicles Processed per episode')
plt.ylabel('Mean speed (m/s)')
plt.show()






