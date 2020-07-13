test = open("stateValues.xml", "w")

for i in range(0, 65536):
    test.write("{0:b}".format(i).zfill(16))
    test.write("\n")