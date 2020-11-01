totalEps = open("totalEps.txt", "r")
t = totalEps.read()
totalEps.close()
t = int(t)+1
totalEps = open("totalEps.txt", "w")
totalEps.write(str(t))
totalEps.close()