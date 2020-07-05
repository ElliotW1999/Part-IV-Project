import matplotlib.pyplot as plt

tripdata = open("tripinfo.xml", "r")
tripDuration = []
for line in tripdata:
    line = line.split(' ')
    if len(line) > 4:
        if line[4] == "<tripinfo":
            print(line[17].split("\"")[1])
            tripDuration.append(float(line[17].split("\"")[1]))
binsvalues = []
binsvalues.append(0)
#binsvalues.append(1)
for i in range(1,11):
    binsvalues.append(int(max(tripDuration)*i/10))

print(binsvalues)
plt.hist(tripDuration, bins=binsvalues)
plt.show()