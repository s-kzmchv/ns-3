import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

numOfSeeds = 1
totalTime = 700
nGateways = 1
discRadius = 5
usPacketSize = 10+13
usDataPeriod = 700
sizeSF = 5

point = [200, 250, 300]
numOfSteps = len(point)

os.system("rm -rf parse_phytx_trace_per_simulation.csv")

for z in range(sizeSF + 1):


    SF = 0 - z
    if (SF == -1):
        break

    arrOfSeeds = np.random.randint(99999, size=numOfSeeds)
    counter = 1
    for i in arrOfSeeds:
        print(counter)
        for j in point:
            os.system("rm -rf tmp")
            os.system("mkdir tmp")
            os.system(" ./waf --run=lorawan-example-tracing --command-template=\"%s --randomSeed={} --nEndDevices={}"
                      " --nGateways={} --discRadius={} --totalTime={} --nRuns=1 --drCalcMethodIndex=2"
                      " --drCalcFixedDRIndex={} --usPacketSize={} --usDataPeriod={}"
                      " --usConfirmedData=0 --dsDataGenerate=0 --verbose=0 --stdcout=0"
                      " --tracePhyTransmissions=1 --tracePhyStates=1 --traceMacPackets=1"
                      " --traceMacStates=1 --traceEDMsgs=1 --traceNSDSMsgs=1 --dsConfirmedData=0"
                      " --outputFileNamePrefix=tmp/myTest\"".format(i,j,nGateways,discRadius,
                                                                                       totalTime,SF,usPacketSize,
                                                                                       usDataPeriod))
            os.system("python3 parse_phytx_trace.py tmp/*trace-phy-tx.csv")
        counter+=1

    fName = "parse_phytx_trace_per_simulation.csv"

    d = pd.read_csv(fName, header = None)
    valuePDR = d[9].values
    averagePDR = [0]*numOfSteps

    for i in range(numOfSeeds):
        for j in range(numOfSteps):
            averagePDR[j] += float(valuePDR[z*(numOfSeeds*numOfSteps) + i*(numOfSteps) + j + 1])


    averagePDR[:] = [x / numOfSeeds for x in averagePDR]

    x = point

    _lambda = 1 / usDataPeriod

    t_64ms = [0.279347, 0.156058, 0.69837, 0.39014, 0.21555, 0.11802]


    y_teor1 = []
    for i in point:
        y_teor1.append(math.exp(-_lambda * i * t_64ms[SF]))

    y_teor2 = []
    for i in point:
        y_teor2.append(math.exp(-2 * _lambda * i * t_64ms[SF]))


    print('значение графика: ' + str(averagePDR))
    print('значение верхней гр: ' + str(y_teor1))
    print('значение нижней гр: ' + str(y_teor2))

    plt.plot(x, averagePDR,  color="g", marker='o',  label = "Результы моделирования")
    plt.plot(x, y_teor1,  color="b", linestyle="dashed", label = "Верхняя граница")
    plt.plot(x, y_teor2, color="r", linestyle="dashed", label="Нижняя граница")


    plt.xlabel("Число конечных устройств")
    plt.ylabel("Вероятность доставки")
    plt.grid()
    plt.legend()
    correctSF = 12 - SF
    plt.savefig("SF{}".format(correctSF))
    plt.show()