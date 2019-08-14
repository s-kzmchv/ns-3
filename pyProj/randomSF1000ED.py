import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import datetime
import csv

def do(nRunsInTime,discRadius,numED,nRunsInTime_withoutOPT ):
    now = datetime.datetime.now()
    print (now.strftime("%d-%m-%Y %H:%M"))

    # os.system("./waf configure")

    # nRunsInTime = 500
    totalTime = 300*nRunsInTime #Время моделирования для одного запуска в секундах
    nGateways = 1 # кол-во шлюзов
    # discRadius = 3000 #Радиус диска (в метрах), в котором размещены конечные устройства и шлюзы
    usPacketSize = 10 + 13  #размер пакета в байтах + 13 байт доп инфы?
    usDataPeriod = 300 #Период между последующими передачами данных восходящего потока с конечного устройства
    x = ["7","8","9","10","11","12"]
    t_23ms = [1.48275, 0.8233, 0.37069, 0.20582, 0.11315, 0.0617]
    random = np.random.randint(99999)
    # random = 1
    # numED = 3000 #Количество конечных устройств

    # Моделирование с оптимизацией

    nRuns = 1 # Количество сеансов моделирования
    OPT = 1
    resOfModelingProbForSF = [0, 0, 0, 0, 0, 0]
    PDR = 0




    os.system("rm -rf parse_phytx_trace_per_enddevice.csv")
    os.system("rm -rf parse_phytx_trace_per_simulation.csv") #очистка output

    os.system("rm -rf tmp")
    os.system("mkdir tmp")
    os.system(" ./waf --run=lorawan-example-tracing --command-template=\"%s --randomSeed={} --nEndDevices={}"
              " --nGateways={} --discRadius={} --totalTime={} --nRuns={} --drCalcMethodIndex=0 --drCalcPerLimit=0.01"
              " --drCalcFixedDRIndex={} --usPacketSize={} --usDataPeriod={}"
              " --usConfirmedData=0 --dsDataGenerate=0 --verbose=0 --stdcout=0"
              " --tracePhyTransmissions=1 --tracePhyStates=1 --traceMacPackets=1"
              " --traceMacStates=1 --traceEDMsgs=1 --traceNSDSMsgs=1 --dsConfirmedData=0"
              " --outputFileNamePrefix=tmp/myTest\"".format(random,numED,nGateways,discRadius,
                                                                               totalTime,nRuns,OPT,usPacketSize,
                                                                               usDataPeriod))
    os.system("python3 parse_phytx_trace.py tmp/*trace-phy-tx.csv")
    # exit(0)
    print("\n ------------------------------------------------------------------------------------------------------- \n")

    fName = "parse_phytx_trace_per_simulation.csv"
    probabilityForSF = pd.read_csv(fName, header = None)
    for j in range(nRuns):
        for i in range(len(t_23ms)):
            # print("probability for SF{} = {} ({}/{}) modeling".format(12 - i, probabilityForSF[10 + 2 + i*3][1],probabilityForSF[10 + + i*3][1],probabilityForSF[10 + + i*3 +1][1]))
            # resOfModelingProbForSF.append(float(probabilityForSF[10 + 2 + i*3][1]))
            resOfModelingProbForSF[i] += (float(probabilityForSF[10 + 2 + i * 3][j+1]))
        PDR += float(probabilityForSF[9][j+1])
        # print("!!!!!!!!!!!!!!!!!!" + probabilityForSF[9][j+1])
    resOfModelingProbForSF[:] = [x / nRuns for x in resOfModelingProbForSF]

    print("\n ############################################################################################################## \n")
    PDR = PDR/nRuns
    print()
    print("PDR = {} on discRadius {}m ".format(PDR, discRadius))
    print()
    print("res of modeling (prob): ")
    print(resOfModelingProbForSF[::-1])

    print("\n !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! TEOR \n")


    _lambda = 1 / usDataPeriod
    numOfSF = [0, 0, 0, 0, 0, 0]
    tmpName = ""
    for file in os.listdir("/dope/forStudy/ns-3/tmp/"):
        if file.endswith("nodes.csv"):
            # print(file)
            tmpName = file
            break

    fName = "/dope/forStudy/ns-3/tmp/" + tmpName

    tmp = pd.read_csv(fName, header = None)
    valueSF = tmp[5].values


    for i in range(numED):
        numOfSF[(int)(valueSF[i+2])] += 1

    print()
    for i in range(len(numOfSF)):
        print("SF{} = {}".format(12-i,numOfSF[i] ))


    PDRTeorLOW = 0
    PDRTeorUP = 0
    y_teorUpper = []
    y_teorLower = []
    for i in range(len(t_23ms)):
        tmp = math.exp(-_lambda * numOfSF[i] * t_23ms[i])
        y_teorUpper.append(tmp)
        PDRTeorUP += (numOfSF[i] * tmp) / numED
        tmp = math.exp(-2 * _lambda * numOfSF[i] * t_23ms[i])
        y_teorLower.append(tmp)
        PDRTeorLOW += (numOfSF[i] * tmp) / numED



    print("teor prob up bound: ")
    print(y_teorUpper[::-1])
    print("teor prob low bound: ")
    print(y_teorLower[::-1])
    print()
    print("Teor PDR low = {}".format(PDRTeorLOW))
    print("Teor PDR up = {}".format(PDRTeorUP))
    print()



    plt.plot(x, resOfModelingProbForSF[::-1],  color="purple", marker='o',  label = "Результы моделирования")
    plt.plot(x, y_teorUpper[::-1],  color="b", linestyle="dashed", label = "Верхняя граница")
    plt.plot(x, y_teorLower[::-1], color="r", linestyle="dashed", label="Нижняя граница")


    plt.xlabel("SF")
    plt.ylabel("Вероятность доставки")
    plt.grid()
    plt.legend()
    plt.savefig("resultOfmodeling/{}_{}_{}.png".format(numED,discRadius,nRunsInTime))
    plt.show()


    now = datetime.datetime.now()
    print (now.strftime("%d-%m-%Y %H:%M"))



    # Моделирование без оптимизации

    # nRunsInTime_withoutOPT = 10
    totalTime = 300*nRunsInTime_withoutOPT #Время моделирования для одного запуска в секундах


    nRuns_withoutOPT = 1 # Количество сеансов моделирования
    OPT = 0
    resOfModelingProbForSF_withoutOPT = [0, 0, 0, 0, 0, 0]
    PDR_withoutOPT = 0




    os.system("rm -rf parse_phytx_trace_per_enddevice.csv")
    os.system("rm -rf parse_phytx_trace_per_simulation.csv") #очистка output

    os.system("rm -rf tmp")
    os.system("mkdir tmp")
    os.system(" ./waf --run=lorawan-example-tracing --command-template=\"%s --randomSeed={} --nEndDevices={}"
              " --nGateways={} --discRadius={} --totalTime={} --nRuns={} --drCalcMethodIndex=0 --drCalcPerLimit=0.01"
              " --drCalcFixedDRIndex={} --usPacketSize={} --usDataPeriod={}"
              " --usConfirmedData=0 --dsDataGenerate=0 --verbose=0 --stdcout=0"
              " --tracePhyTransmissions=1 --tracePhyStates=1 --traceMacPackets=1"
              " --traceMacStates=1 --traceEDMsgs=1 --traceNSDSMsgs=1 --dsConfirmedData=0"
              " --outputFileNamePrefix=tmp/myTest\"".format(random,numED,nGateways,discRadius,
                                                                               totalTime,nRuns_withoutOPT,OPT,usPacketSize,
                                                                               usDataPeriod))
    os.system("python3 parse_phytx_trace.py tmp/*trace-phy-tx.csv")

    print("\n ------------------------------------------------------------------------------------------------------- \n")

    fName = "parse_phytx_trace_per_simulation.csv"
    probabilityForSF = pd.read_csv(fName, header = None)
    for j in range(nRuns_withoutOPT):
        for i in range(len(t_23ms)):
            # print("probability for SF{} = {} ({}/{}) modeling".format(12 - i, probabilityForSF[10 + 2 + i*3][1],probabilityForSF[10 + + i*3][1],probabilityForSF[10 + + i*3 +1][1]))
            # resOfModelingProbForSF.append(float(probabilityForSF[10 + 2 + i*3][1]))
            resOfModelingProbForSF_withoutOPT[i] += (float(probabilityForSF[10 + 2 + i * 3][j+1]))
        PDR_withoutOPT+= float(probabilityForSF[9][j+1])
        # print("!!!!!!!!!!!!!!!!!!" + probabilityForSF[9][j+1])
    resOfModelingProbForSF_withoutOPT[:] = [x / nRuns_withoutOPT for x in resOfModelingProbForSF_withoutOPT]

    print("\n ############################################################################################################## \n")
    PDR_withoutOPT = PDR_withoutOPT/nRuns_withoutOPT
    print()
    print("PDR = {} on discRadius {}m ".format(PDR_withoutOPT, discRadius))
    print()
    print("res of modeling (prob): ")
    print(resOfModelingProbForSF_withoutOPT[::-1])

    print("\n !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! TEOR \n")


    _lambda = 1 / usDataPeriod
    numOfSF_withoutOPT = [0, 0, 0, 0, 0, 0]
    tmpName = ""
    for file in os.listdir("/dope/forStudy/ns-3/tmp/"):
        if file.endswith("nodes.csv"):
            # print(file)
            tmpName = file
            break

    fName = "/dope/forStudy/ns-3/tmp/" + tmpName

    tmp = pd.read_csv(fName, header = None)
    valueSF = tmp[5].values


    for i in range(numED):
        numOfSF_withoutOPT[(int)(valueSF[i+2])] += 1

    print()
    for i in range(len(numOfSF_withoutOPT)):
        print("SF{} = {}".format(12-i,numOfSF_withoutOPT[i] ))


    PDRTeorLOW_withoutOPT = 0
    PDRTeorUP_withoutOPT = 0
    y_teorUpper_withoutOPT = []
    y_teorLower_withoutOPT = []
    for i in range(len(t_23ms)):
        tmp = math.exp(-_lambda * numOfSF_withoutOPT[i]  * t_23ms[i])
        y_teorUpper_withoutOPT.append(tmp)
        PDRTeorUP_withoutOPT += (numOfSF_withoutOPT[i]  * tmp) / numED
        tmp = math.exp(-2 * _lambda * numOfSF_withoutOPT[i]  * t_23ms[i])
        y_teorLower_withoutOPT.append(tmp)
        PDRTeorLOW_withoutOPT += (numOfSF_withoutOPT[i] * tmp) / numED



    print("teor prob up bound: ")
    print(y_teorUpper_withoutOPT[::-1])
    print("teor prob low bound: ")
    print(y_teorLower_withoutOPT[::-1])
    print()
    print("Teor PDR low = {}".format(PDRTeorLOW_withoutOPT))
    print("Teor PDR up = {}".format(PDRTeorUP_withoutOPT))
    print()



    plt.plot(x, resOfModelingProbForSF_withoutOPT[::-1],  color="purple", marker='o',  label = "Результы моделирования")
    plt.plot(x, y_teorUpper_withoutOPT[::-1],  color="b", linestyle="dashed", label = "Верхняя граница")
    plt.plot(x, y_teorLower_withoutOPT[::-1], color="r", linestyle="dashed", label="Нижняя граница")


    plt.xlabel("SF")
    plt.ylabel("Вероятность доставки")
    plt.grid()
    plt.legend()
    plt.savefig("resultOfmodeling/{}_{}_{}_NoOPT.png".format(numED,discRadius,nRunsInTime_withoutOPT))
    plt.show()


    now = datetime.datetime.now()
    print (now.strftime("%d-%m-%Y %H:%M"))



    fieldnames = [str(numED), str(discRadius), str(nRunsInTime_withoutOPT), str(nRunsInTime),
                  str(PDR_withoutOPT).replace('.',','), str(PDRTeorUP_withoutOPT).replace('.',','), str(PDRTeorLOW_withoutOPT).replace('.',','), str(resOfModelingProbForSF_withoutOPT),
                  str(PDR).replace('.',','), str(PDRTeorUP).replace('.',','), str(PDRTeorLOW).replace('.',','),str(resOfModelingProbForSF)]
    path = "resultOfmodeling/table.csv"

    with open(path, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)

if __name__ == "__main__":
    do(500,1500,3000,25)
    # do(1000,1500,3000,25)
    # do(1,3000,1000,1)
    # do(1,3000,3000,1)
