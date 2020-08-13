import matplotlib.pyplot as plt
import numpy 

tripdata = open("tripinfoRL.xml", "r")
timeLoss = []
timeStopped = []
for line in tripdata:
    line = line.split(' ')
    if len(line) > 4:
        if line[4] == "<tripinfo":
            timeLoss.append(float(line[20].split("\"")[1]))
            timeStopped.append(float(line[17].split("\"")[1]))
            
            
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


lossCurves = open("generateLossCurves.csv", "r")
lossPerEpisode= []

i = 0
for line in lossCurves:
    line = line.split(" ")
    lossPerEpisode.append(float(line[0]))

avgLoss = []
for i in range (0, 9):
    avgLoss.append(lossPerEpisode[1])
i = 0
for i in range(10, len(lossPerEpisode)-1):
    x =( lossPerEpisode[i] + lossPerEpisode[i-1] + lossPerEpisode[i-2] + lossPerEpisode[i-3] + lossPerEpisode[i-4] + lossPerEpisode[i-5] + lossPerEpisode[i-6] + lossPerEpisode[i-7] + lossPerEpisode[i-8] + lossPerEpisode[i-9] )/10
    avgLoss.append(x)


plt.plot( lossPerEpisode)
plt.plot( avgLoss)
plt.title('Loss per episode')
plt.xlabel('episode number')
plt.ylabel('Time loss (s)')
plt.show()

delta = []
learningUpdates = open("learningUpdates.csv", "r")
for line in learningUpdates:
    delta.append(float(line))
    


plt.plot( delta)
plt.title('learning Updates per episode')
plt.xlabel('episode number')
plt.ylabel('change in Q values')
plt.show()


print(numpy.mean(timeLoss))
print(numpy.std(timeLoss))

print(numpy.mean(timeStopped))
print(numpy.std(timeStopped))
print(len(timeLoss))






