from request import request
import config
import time
import random

#Converts a log file of XY coordinates to node numbers and returns a reduced
#List of lists that contains the log information in its elements. 
#Ex.     S|D |#|V|tStamp
#       [1,15,1,4 , 0  ],
#       [2,3,2,3  , 30 ],...
#Then it turns them into request objects and puts them in the list.
def convXYtoNode(logFile):
    benchmark = []

    with open(logFile,"r") as bmread:
        for line in bmread:
            benchmarkLine = []
            benchmarkItems = line.split()
            for i in benchmarkItems:
                benchmarkLine.append(int(float(i)))
            benchmark.append(benchmarkLine)
    newBenchmark = []
    newConfiguration = []
    ## Converts the XY coordinates
    ## To reconfigure the nodes, comment out these equations and uncomment the next section
    #(1 0) = 0; (1 1) = 1; (1 2) = 2; (1 3) = 3; (1 4) = 4; (1 5) = 5; (1 6) = 6; (1 7) = 7
    #(2 7) = 8; (2 6) = 9; (2 5) = 10; (2 4) = 11; (2 3) = 12; (2 2) = 13; (2 1) = 14; (2 0) = 15

    for row in benchmark:
        if (row[0] != 0) & (row[2] != 0):
            if (row[0] == 1) & (row[2] == 1):
                newRow = [(row[0] - 1) * 8 + row[1], (row[2] - 1) * 8 + row[3]]
            elif (row[0] == 2) & (row[2] == 2):
                newRow = [(row[0] - 1) * 8 + (7 - row[1]), (row[2] - 1) * 8 + (7 - row[3])]
            elif (row[0] == 1) & (row[2] == 2):
                newRow = [(row[0] - 1) * 8 + row[1], (row[2] - 1) * 8 + (7 - row[3])]
            elif (row[0] == 2) & (row[2] == 1):
                newRow = [(row[0] - 1) * 8 + (7 - row[1]), (row[2] - 1) * 8 + row[3]]   
            newRow.extend(row[4:6])
            newRow.append(row[6]*config.EccToOcc)
            #print (newRow)
            newBenchmark.append(request(newRow))
    requestsHolder = newBenchmark
            
    return newBenchmark

#Get a file of configurations and put it into a list
def readConfigurations(logFile):
    allConfigurations = []
    
    with open(logFile,"r") as theConfigurations:
        for line in theConfigurations:
            networkLine = []
            networkNodes = line.split(',')
            for j in networkNodes:
                networkLine.append(int(float(j)))
            allConfigurations.append(networkLine)
            
    return allConfigurations


#Pre-Condition: Number of nodes to be used is input into function
#Post: A list of unique random numbers from 0 to the number of nodes -1 is returned
def generateKey(nodeCount):
    random.seed()
    key = []
    while len(key) < nodeCount:
        randNum = random.randint(0,15)
        uniqueCheck = [False]* len(key)
        if len(key) > 0:
            for i in range(0,len(key)):
                if randNum != key[i]:
                    uniqueCheck[i] = True
            if uniqueCheck[0:len(key)] == [True]*len(uniqueCheck):
                key.append(randNum)

        else:
            key.append(randNum)
    return key

def writeResults(dataLine):
    #S,  D,  V,  Time Received, Time Started, Direction, Time Ended, Wait Time, Cost
    with open((str(times) + ".txt"),"a") as resultFile:
        resultFile.write('{} {:5}'.format(str(dataLine.toString()), str(dataLine.get_Direction())) + "\n")


#Go through the directory and find the file to be tested
for i in range(0,len(config.benchmarks)):
    #If the file tested == the file the loop is on break. else continue
    if config.logFile == str(config.benchmarksOnly[i]):
        logFile = config.benchmarks[i]
        
    if config.configurationFile == str(config.benchmarksOnly[i]):
        theConfigurationFile = config.benchmarks[i]
    else:
        continue

#Get Time       
startTime = time.time()

#Set to 0 to run a file of different configurations
#Set to 1 to run one configuration that you want (change the code after this line)
#Set to any higher number to run it as many times as the number you entered with random configs each time
numberOfConfigurations = 1 #Set how many different configurations you want to test

#Set each core's position
zeroPosition = 0
onePosition = 1
twoPosition = 2
threePosition = 3
fourPosition = 4
fivePosition = 5
sixPosition = 6
sevenPosition = 7
eightPosition = 8
ninePosition = 9
tenPosition = 10
elevenPosition = 11
twelvePosition = 12
thirteenPosition = 13
fourteenPosition = 14
fifteenPosition = 15

#If there is a configuration file then use it
if (config.configurationFile != '') & (numberOfConfigurations == 0):
    differentConfigurations = readConfigurations(theConfigurationFile) #get all the configurations
    numberOfConfigurations = len(differentConfigurations) #run as many times as there are configurations


#Go through the whole file with a different configuration as many times as you tell it to unless given a file
for times in range(0, numberOfConfigurations):
    
    #Get a new list of request objects
    config.activeReq = convXYtoNode(logFile)
    listLen = len(config.activeReq) #How many lines of data there are to be processed

    #Print the file info
    print 'Running benchmark ' + logFile + '\n'
    print 'ListLength:' + str(listLen) + '\n' + '\n' + '\n'

    #If you only wanted to run one specific configuration
    if numberOfConfigurations == 1:
        #Set the configuration
        theConfiguration = [zeroPosition, onePosition, twoPosition, threePosition, fourPosition,
                            fivePosition, sixPosition, sevenPosition, eightPosition, ninePosition,
                            tenPosition, elevenPosition, twelvePosition, thirteenPosition,
                            fourteenPosition, fifteenPosition]

    elif numberOfConfigurations == len(differentConfigurations):
        #Set the configuration
        theConfiguration = differentConfigurations[times]
        
    #else run a random one
    else:
        #All the different nodes
        theChoices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        #Select a random node and put it in each position then take it out of the selections
        zeroPosition = random.choice(theChoices)
        theChoices.remove(zeroPosition)
        onePosition = random.choice(theChoices)
        theChoices.remove(onePosition)
        twoPosition = random.choice(theChoices)
        theChoices.remove(twoPosition)
        threePosition = random.choice(theChoices)
        theChoices.remove(threePosition)
        fourPosition = random.choice(theChoices)
        theChoices.remove(fourPosition)
        fivePosition = random.choice(theChoices)
        theChoices.remove(fivePosition)
        sixPosition = random.choice(theChoices)
        theChoices.remove(sixPosition)
        sevenPosition = random.choice(theChoices)
        theChoices.remove(sevenPosition)
        eightPosition = random.choice(theChoices)
        theChoices.remove(eightPosition)
        ninePosition = random.choice(theChoices)
        theChoices.remove(ninePosition)
        tenPosition = random.choice(theChoices)
        theChoices.remove(tenPosition)
        elevenPosition = random.choice(theChoices)
        theChoices.remove(elevenPosition)
        twelvePosition = random.choice(theChoices)
        theChoices.remove(twelvePosition)
        thirteenPosition = random.choice(theChoices)
        theChoices.remove(thirteenPosition)
        fourteenPosition = random.choice(theChoices)
        theChoices.remove(fourteenPosition)
        fifteenPosition = theChoices[0]

        #Set the configuration
        theConfiguration = [zeroPosition, onePosition, twoPosition, threePosition, fourPosition,
                            fivePosition, sixPosition, sevenPosition, eightPosition, ninePosition,
                            tenPosition, elevenPosition, twelvePosition, thirteenPosition,
                            fourteenPosition, fifteenPosition]
        

    #Write the information of the file
    with open((str(times) + ".txt"),"a") as resultFile:
        resultFile.write("\n" + str(times) + "\n" + str(logFile) + "\n" + str(listLen)
                         + "\n" + str(theConfiguration) + "\n")        
    
    t = 0 #Monitor optical clock Cycles
    canSchedule = False #Monitor if there is room for the request
    activeRequests = [] #Keeps a hold of the requests in the network
    sourceNodeTracker = [] #Keeps track of source nodes
    destinationNodeTracker = [] #Keeps track of destination nodes
    cost = 0 #The volume * the distance of a request
    nextTimeStamp = 0
    thisTimeStamp = 0
    lowestVolume = int(10000000)

    #While there are requests to be processed
    while (config.activeReq != []):
            
        network1ToString = str(config.nodestate1)
        network2ToString = str(config.nodestate2)
        network3ToString = str(config.nodestate3)
        
        #If there are requests in the network
        if (len(activeRequests) > 0):

            difference = (nextTimeStamp - thisTimeStamp)
            if (lowestVolume >= difference) & (network1ToString.find('0, 0') != -1):
                lowestVolume = difference
                if difference <= 0:
                    lowestVolume = 1

            #Go through each request
            for requests in activeRequests:
                #If the volume is greater than zero, reduce it by one. Otherwise, remove it
                t += lowestVolume
                if (network1ToString.find('0, 0') == -1):
                    if config.frequencies == 1:
                        requests.set_volumeTrack(lowestVolume)
                    else:
                        if (network2ToString.find('0, 0') == -1):
                            if config.frequencies == 2:
                                requests.set_volumeTrack(lowestVolume)
                            else:
                                if (network3ToString.find('0, 0') == -1):
                                    requests.set_volumeTrack(lowestVolume)
                                    
                elif (requests.get_volumeTrack() > 0):
                    requests.set_volumeTrack(lowestVolume) #sets the volume to the original - 1
                    
                if (requests.get_volumeTrack() <= 0):
                    index = config.activeReq.index(requests) #Find the request in the actual list
                    config.activeReq[index].set_endTime(t) #After full trasmition (w/o OccToEcc conversion)
                    config.activeReq[index].set_waitTime()
                    writeResults(config.activeReq[index]) #Write all the info of the data in the file
                    config.activeReq[index].reqProcessing() #Remove the request
                    activeRequests.remove(requests) #Remove the request from the other list
                    sourceNodeTracker.pop(index) #Remove the source node of this data from the list
                    destinationNodeTracker.pop(index) #Remove the dest node of this data from the list
        else:
            t = config.activeReq[0].get_timeStamp()

        counter = -1
        lowestVolume = int(10000000)
        #Go through each request in the file
        for req in config.activeReq:
            counter += 1
            nextTimeStamp = req.get_timeStamp()
            
            #If the request has been received (the time stamp on the request matches the Clock cyles
            #And if it has not been processed yet, so it has a direction of "None", then schedule it
            if (req.get_timeStamp() <= t) & (req.get_Direction() == "None"):
                
                if (req.get_Tag() == False):
                    sourceNodeTracker.append(req.get_sourceNode()) #Add the source node into the list to track it
                    destinationNodeTracker.append(req.get_destNode()) #Add the dest node into the list to track it
                    req.set_theSPosition(theConfiguration.index(req.get_sourceNode())) #Set the position of the source node
                    req.set_theDPosition(theConfiguration.index(req.get_destNode())) #Set the position of the dest node
                    req.set_Tag(True) #Set if the data has been processed

                #If it is the first request from this source node and to this destination node
                if (((sourceNodeTracker[0:counter + 1].count(config.activeReq[counter].get_sourceNode())) <= 1) &
                ((destinationNodeTracker[0:counter + 1].count(config.activeReq[counter].get_destNode())) <= 1)):
                    canSchedule = req.schedule(config.nodestate1, 1) #Schedule it in the first network
                #Else, according to the rules (tetris and wormhole, it can't be scheduled)
                else:
                    canSchedule = False
                
                #If it fits in the network, else move on
                if canSchedule:
                    thisTimeStamp = req.get_timeStamp()
                    if req.get_volumeTrack() < lowestVolume:
                        lowestVolume = req.get_volumeTrack()
                    req.set_Cost() #Set the individual cost
                    cost = cost + (req.get_Cost()) #Add to total cost
                    req.set_startTime(t) #Set the start time since it is started now
                    activeRequests.append(req) #Put it in the list of requests in the network
                else:
                    #If there is more than one network
                    if (config.frequencies > 1):
                        
                        #If it is the first request from this source node and to this destination node
                        if (((sourceNodeTracker[0:counter + 1].count(config.activeReq[counter].get_sourceNode())) <= 1) &
                        ((destinationNodeTracker[0:counter + 1].count(config.activeReq[counter].get_destNode())) <= 1)):
                            canSchedule = req.schedule(config.nodestate2, 2) #Schedule it in the 2nd network
                        #Else, according to the rules (tetris and wormhole, it can't be scheduled)
                        else:
                            canSchedule = False
                            
                        #If it fits in the 2nd network, else move on
                        if canSchedule:
                            thisTimeStamp = req.get_timeStamp()
                            if req.get_volumeTrack() < lowestVolume:
                                lowestVolume = req.get_volumeTrack()
                            req.set_Cost() #Set the individual cost
                            cost = cost + (req.get_Cost()) #Add to total cost
                            req.set_startTime(t) #Set the start time since it is started now
                            activeRequests.append(req) #Put it in the list of requests in the network
                        else:
                            #If there are three networks
                            if (config.frequencies == 3):
                                
                                #If it is the first request from this source node and to this destination node
                                if (((sourceNodeTracker[0:counter + 1].count(config.activeReq[counter].get_sourceNode())) <= 1) &
                                ((destinationNodeTracker[0:counter + 1].count(config.activeReq[counter].get_destNode())) <= 1)):
                                    canSchedule = req.schedule(config.nodestate3, 3) #Schedule it in the 3rd network
                                #Else, according to the rules (tetris and wormhole, it can't be scheduled)
                                else:
                                    canSchedule = False
                                #If it fits in the 3rd network, else move on
                                if canSchedule:
                                    thisTimeStamp = req.get_timeStamp()
                                    if req.get_volumeTrack() < lowestVolume:
                                        lowestVolume = req.get_volumeTrack()
                                    req.set_Cost() #Set the individual cost
                                    cost = cost + (req.get_Cost()) #Add to total cost
                                    req.set_startTime(t) #Set the start time since it is started now
                                    activeRequests.append(req) #Put it in the list of requests in the network
                                else:
                                    continue
                            else:
                                continue
                    else:
                        continue
                    
            #Elif, it has not yet been received (the time stamp is greater than the current clock cycle) then break
            elif (t < req.get_timeStamp()):
                break
            else:
                if req.get_Direction() != "None":
                    if req.get_volumeTrack() < lowestVolume:
                        lowestVolume = req.get_volumeTrack()
                continue



    #Show results
    print 'Finished test file: ' + str(config.logFile)
    print 'Total Optical Clock Cycles: ' + str(t)
    print 'Total Cost: ' + str(cost)
    totalTime = float(t)/(config.OCC*(10**9))
    print 'Runtime: '+ str(totalTime) +'seconds'
    tProgram = time.time()-startTime
    print 'Time for Program: ' + str(tProgram) + '\n\n'
    print '----------------------------------------------------------'

raise SystemExit
