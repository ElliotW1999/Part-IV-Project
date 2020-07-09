import matplotlib.pyplot as plt

tripdata = open("tripinfoEDF.xml", "r")
timeLoss = []
for line in tripdata:
    line = line.split(' ')
    if len(line) > 4:
        if line[4] == "<tripinfo":
            print(line[17].split("\"")[1])
            timeLoss.append(float(line[20].split("\"")[1]))
binsvalues = []
binsvalues.append(0)
#binsvalues.append(1)
for i in range(1,51):
    binsvalues.append(int(max(timeLoss)*i/50))

print(binsvalues)
plt.hist(timeLoss, bins=binsvalues)
plt.show()