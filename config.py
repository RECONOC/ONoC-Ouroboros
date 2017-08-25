import os, sys


# Pre: Requires correct directory of benchmarks in variable path
# Post: Creates list of benchmarks
path = 'C:/Users/nxconrad/Desktop/REU 2.0/Benchmark Data/16-core/7'
dirs = os.listdir(path)
benchmarks = []
benchmarksOnly = []

# Appends all benchmarks in directory into one list

for file in dirs:
    benchmarks.append(file)
    benchmarksOnly.append(file)
for i in range(0,len(benchmarks)):
    benchmarks[i] = path + '/' + benchmarks[i]
nodeCount = 16
activeReq = [] #The list of requests received
nodestate1 = [0]*nodeCount #first frequency loop
nodestate2 = [0]*nodeCount #second frequency loop   
nodestate3 = [0]*nodeCount #third frequency loop
frequencies = 1 #Changes the number of loops that can be used to process requests (Change at will)
OCC = 40 #GHz (Change at will)
ECC = 2 #GHz (Change at will)
packetSize = 8*(10**9) #bits

logFile = 'flow_freqmine100.txt'#'flow_dedup.log'#'test_walston_004.log' the log file that will be tested
configurationFile = 'All Configurations-600.txt' #The file with only configurations in it. (void this when not needed)
weighted_cutoff = 20 # max nodes allowedd to be bypassed on furthest path (Change at will)


#Global time constants to account for certain processes.
checkAvailability = 1 #Constant to check if the channels are available (Change at will)
EccToOcc       = 1 #Constant to turn the electrical signal into an optical one (Change at will)
OccToEcc       = 5 #Constant to turn the optical signal into an electrical one (Change at will)
