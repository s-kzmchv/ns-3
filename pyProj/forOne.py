import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

numOfSeeds = 1
numOfDevice = 20
step = 1
beginDevice = 10

totalTime = 620
nGateways = 1
discRadius = 100
usPacketSize = 51
usDataPeriod = 62

numOfSteps = math.ceil((numOfDevice - beginDevice + 1)/step)

SF = 2

arrOfSeeds = np.random.randint(99999, size=numOfSeeds)

os.system("rm -rf parse_phytx_trace_per_simulation.csv")

for i in arrOfSeeds:

    for j in np.arange(beginDevice, numOfDevice + 1, step):
        os.system("rm -rf tmp")
        os.system("mkdir tmp")
        os.system("./waf --run=lorawan-example-tracing --command-template=\"%s --randomSeed={} --nEndDevices={} --nGateways={} --discRadius={} --totalTime={} --nRuns=1 --drCalcMethodIndex=2 --drCalcFixedDRIndex={} --usPacketSize={} --usDataPeriod={} --usConfirmedData=0 --dsDataGenerate=0  --verbose=0 --stdcout=0 --tracePhyTransmissions=1 --tracePhyStates=1 --traceMacPackets=1 --traceMacStates=1 --outputFileNamePrefix=tmp/myTest\"".format(i,j,nGateways,discRadius,totalTime,SF,usPacketSize,usDataPeriod))
        os.system("python3 parse_phytx_trace.py tmp/*trace-phy-tx.csv")


fName = "parse_phytx_trace_per_simulation.csv"

d = pd.read_csv(fName, header = None)
valuePDR = d[9].values
averagePDR = [0]*numOfSteps
for i in range(numOfSeeds):
    for j in range(numOfSteps):
        # print(valuePDR[i*numOfDevice + j + 1])
        averagePDR[j] += float(valuePDR[i*(numOfSteps) + j + 1])


averagePDR[:] = [x / numOfSeeds for x in averagePDR]


x = np.arange(beginDevice, numOfDevice+1, step)


_lambda = 1/totalTime

t_51ms = [2465.79, 1314.82, 616.45, 328.70, 184.83, 102.66]



y_teor = []
for i in np.arange(beginDevice, numOfDevice + 1, step):
    y_teor.append(math.exp(-1 * _lambda * (i-1) * t_51ms[SF]))
    # print(math.exp(-1 * _lambda * (i-1) * t_51ms[SF]))

plt.plot(x, averagePDR,  color="g", label = "average")
plt.plot(x, y_teor,  color="b", label = "teor")


plt.xlabel("Число конечных устройств")
plt.ylabel("Вероятность доставки")
plt.grid()
plt.legend()
plt.savefig("/home/sam/ns-3-dev-git-lorawan/pyProj/SFforOne{}".format(12-SF))
plt.show()
print (averagePDR)