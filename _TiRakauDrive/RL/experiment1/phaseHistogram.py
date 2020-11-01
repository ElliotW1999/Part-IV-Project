import matplotlib.pyplot as plt

phaseData = open("stateActions.csv", "r")
phases = []
for line in phaseData:
    phases.append(line.split(",")[1].replace('\n',''))

print(phases)
print(len(phases))
binsvalues = [0, 1, 2, 3, 4, 5, 6]

plt.title('Time at suboptimal speed')
plt.xlabel('Time loss (s)')
plt.ylabel('Number of vehs')
plt.hist(phases, bins=binsvalues)
plt.show()