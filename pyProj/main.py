import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt


# NS_LOG=\"LoRaWANPhy\"
# numOfDevice = 51
# step = 10
# beginDevice = 1
# numOfSteps = math.ceil((numOfDevice - beginDevice + 1)/step)

numOfSeeds = 1
totalTime = 700
nGateways = 1
discRadius = 5
usPacketSize = 20
usDataPeriod = 700
sizeSF = 5

# point = [ 3]
# point = [200, 700, 1400, 2200, 3100, 3600]
point = [200, 500, 1000, 2000, 3000]
# point = [200, 500, 1000]

# point = [2, 5, 10, 20, 30]
# point = [2, 7, 14, 22, 31, 36]
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

    forMathLab = {}
    for j in range(numOfSteps):
        forMathLab[j] = []

    for i in range(numOfSeeds):
        for j in range(numOfSteps):
            forMathLab[j].append(float(valuePDR[z*(numOfSeeds*numOfSteps) + i*(numOfSteps) + j + 1 ]))
            averagePDR[j] += float(valuePDR[z*(numOfSeeds*numOfSteps) + i*(numOfSteps) + j + 1])
            # print(averagePDR[j])


    averagePDR[:] = [x / numOfSeeds for x in averagePDR]
    for curr in forMathLab:
        print(str(point[curr]) + ': ' + str(forMathLab[curr]))

    # x = np.arange(beginDevice, numOfDevice+1, step)

    x = point

    _lambda = 1 / usDataPeriod

    t_51ms = [1.97427, 0.156058, 0.57549, 0.39014, 0.21555, 0.11802] #0.12314 1.97427

    print(t_51ms[SF])
    print(SF)

    # y_need1WithDef = []
    # for i in point:
    #     y_need1WithDef.append(math.exp(-_lambda * i * 0.12314))
    #
    # y_need12WithDef = []
    # for i in point:
    #     y_need12WithDef.append(math.exp(-_lambda * i * 2.138112008))
    #
    # y_need12WithOUTDef = []
    # for i in point:
    #     y_need12WithOUTDef.append(math.exp(-_lambda * i * 1.974272))

    y_teor1 = []
    for i in point:
        y_teor1.append(math.exp(-_lambda * i * t_51ms[SF]))
        # print(math.exp(-1 * _lambda * (i-1) * t_51ms[SF]))

    y_teor2 = []
    for i in point:
        y_teor2.append(math.exp(-2 * _lambda * i * t_51ms[SF]))
        # print(math.exp(-1 * _lambda * (i-1) * t_51ms[SF]))

    y_teor3 = []
    for i in point:
        y_teor3.append(math.exp(-2 * _lambda * i * t_51ms[SF]) + 0.7*0.55555 *_lambda * i * 2 * t_51ms[SF] * math.exp(-2 * _lambda * i * t_51ms[SF]))
        # print(math.exp(-1 * _lambda * (i-1) * t_51ms[SF]))


    # y_teor4 = [0.9954, 0.7804, 0.7589, 0.6438, 0.5000, 0.4431]
    y_teor4 = [0.5578, 0.2044, 0.0502, 0.003, 0.0003]

    print('значение графика: ' + str(averagePDR))
    print('значение верхней гр: ' + str(y_teor1))
    print('значение нижней гр: ' + str(y_teor2))

    plt.plot(x, y_teor4, color="g", marker='o', label="Результы моделирования с имитацией защиты")
    plt.plot(x, averagePDR,  color="purple", marker='o',  label = "Результы моделирования без имитации защиты")
    plt.plot(x, y_teor1,  color="b", linestyle="dashed", label = "Верхняя граница")
    plt.plot(x, y_teor2, color="r", linestyle="dashed", label="Нижняя граница")
    # plt.plot(x, y_teor3, color="purple", marker='o', label="Теор формула")

    # plt.plot(x, y_teor1, color="r", linestyle="dashed", label="Верхняя 64 7")
    # plt.plot(x, y_need1WithDef, color="g", linestyle="dashed", label="Верхняя 68 7")
    # plt.plot(x, y_need12WithOUTDef, color="b", linestyle="dashed", label="Верхняя 47 12")
    # plt.plot(x, y_need12WithDef, color="purple", linestyle="dashed", label="Верхняя 51 12")

    plt.xlabel("Число конечных устройств")
    plt.ylabel("Вероятность доставки")
    plt.grid()
    plt.legend()
    correctSF = 12 - SF
    plt.savefig("/dope/forStudy/diplom/ns-3-dev-git-lorawan/pyProj/SF{}".format(correctSF))
    plt.show()