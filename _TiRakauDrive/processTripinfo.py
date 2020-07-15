import matplotlib.pyplot as plt

tripdata = open("output/tripinfoEDF.xml", "r")
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
