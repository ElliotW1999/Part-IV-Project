test = open("stateActionValues.csv", "w")
for n in range(0, 9):
    for m in range(0, 10):
        for i in range(0, 7):
            for k in range(0, 9):
                test.write(str(n)+str(m)+str(i)+str(k)+"    ,") #remove?
                for l in range(0, 7):               # actions init at 0.0 for exploration 
                    test.write("0.0,")
                test.write("\n")
	
    
if False: 
    for i in range(0, 7):
        for k in range(0, 9):
            #test.write(str(i)+str(k)+",") #remove?
            for j in range (0, 513):
                if j == 512:
                    test.write("1.0     ")
                else:
                    test.write("0.0,    ")
            test.write("\n")
    #test.write("0")
    for i in range(0,256): # remove?
        x = str(bin(i).zfill(10))
        x = x.replace('b','0')
        x = x[2:10]
        #test.write(","+x)
    #test.write(",sum\n")
    #test = open("stateValues.csv", "w")
    import pandas as pd
    #test.write("0")

    states = []
    phaseGroups = []
    for j in range (0, 256):
        loopDets = []
        #test.write(str(i)+str(k)+",")
        for i in range(0, 7):
            for k in range(0, 9):
                loopDets.append(0)
                #if j == 255:
                    #test.write("0")
                #else:
                    #test.write("0,")
            #test.write("\n")
        phaseGroups.append(loopDets)
        
    for i in range(0, 7):
        for k in range(0, 9):
            states.append(str(i)+str(k))
        
    #print(phaseGroups)
        #for i in range(0, 65536):
        #test.write("{0:b}".format(i).zfill(16))
        #test.write("\n")
        
    dict = {
        'State' : states
        
    }

    for i in range(0,256):
        x = str(bin(i).zfill(10))
        x = x.replace('b','0')
        x = x[2:10]
        print(i)
        dict[x] = phaseGroups[i]
    dict['Sum'] = phaseGroups[0]
       
    df = pd.DataFrame(dict)
    df.to_csv('stateValues.csv')