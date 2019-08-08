import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

# os.system("./waf configure")


numOfSeeds = 1 #кол-во сидов
totalTime = 301 #Время моделирования для одного запуска в секундах
nGateways = 1 # кол-во шлюзов
discRadius = 1500 #Радиус диска (в метрах), в котором размещены конечные устройства и шлюзы
usPacketSize = 10 + 13  #размер пакета в байтах + 13 байт доп инфы?
usDataPeriod = 300 #Период между последующими передачами данных восходящего потока с конечного устройства
nRuns = 10 # Количество сеансов моделирования



point = [1000] #Количество конечных устройств
numOfSteps = len(point)

t_23ms = [1.48275, 0.8233, 0.37069, 0.20582, 0.11315, 0.0617]
resOfModelingProbForSF = [0, 0, 0, 0, 0, 0]
numOfSF = [0, 0, 0, 0, 0, 0]

arrOfSeeds = np.random.randint(99999, size=numOfSeeds)
counter = 0

PDR = 0
for random in arrOfSeeds:
    counter +=1
    print(counter)
    os.system("rm -rf parse_phytx_trace_per_enddevice.csv")
    os.system("rm -rf parse_phytx_trace_per_simulation.csv") #очистка output

    os.system("rm -rf tmp")
    os.system("mkdir tmp")
    os.system(" ./waf --run=lorawan-example-tracing --command-template=\"%s --randomSeed={} --nEndDevices={}"
              " --nGateways={} --discRadius={} --totalTime={} --nRuns=1 --drCalcMethodIndex=0 --drCalcPerLimit=0.01"
              " --drCalcFixedDRIndex={} --usPacketSize={} --usDataPeriod={}"
              " --usConfirmedData=0 --dsDataGenerate=0 --verbose=0 --stdcout=0"
              " --tracePhyTransmissions=1 --tracePhyStates=1 --traceMacPackets=1"
              " --traceMacStates=1 --traceEDMsgs=1 --traceNSDSMsgs=1 --dsConfirmedData=0"
              " --outputFileNamePrefix=tmp/myTest\"".format(random,point[0],nGateways,discRadius,
                                                                               totalTime,5,usPacketSize,
                                                                               usDataPeriod))
    os.system("python3 parse_phytx_trace.py tmp/*trace-phy-tx.csv")
    # os.system("python3 parse_nodes.py tmp/*nodes.csv")

    print("\n ------------------------------------------------------------------------------------------------------- \n")

    tmpName = ""
    for file in os.listdir("/home/developer/Project/tmp/"):
        if file.endswith("nodes.csv"):
            # print(file)
            tmpName = file
            break

    fName = "/home/developer/Project/tmp/" + tmpName

    tmp = pd.read_csv(fName, header = None)
    valueSF = tmp[5].values


    for i in range(point[0]):
        numOfSF[(int)(valueSF[i+2])] += 1

    print()
    for i in range(len(numOfSF)):
        print("SF{} = {}".format(12-i,numOfSF[i] / counter))


    fName = "parse_phytx_trace_per_simulation.csv"

    probabilityForSF = pd.read_csv(fName, header = None)
    PDR += float(probabilityForSF[9][1])
    for i in range(len(t_23ms)):
        print("probability for SF{} = {} ({}/{}) modeling".format(12 - i, probabilityForSF[10 + 2 + i*3][1],probabilityForSF[10 + + i*3][1],probabilityForSF[10 + + i*3 +1][1]))
        # resOfModelingProbForSF.append(float(probabilityForSF[10 + 2 + i*3][1]))
        resOfModelingProbForSF[i] += (float(probabilityForSF[10 + 2 + i * 3][1]))


resOfModelingProbForSF[:] = [x / numOfSeeds for x in resOfModelingProbForSF]

print("\n ############################################################################################################## \n")


print()
print("PDR = {} on discRadius {}m ".format(PDR/numOfSeeds, discRadius))
print()
print("res of modeling (prob): ")
print(resOfModelingProbForSF[::-1])


_lambda = 1 / usDataPeriod

y_teorUpper = []
for i in range(len(t_23ms)):
    y_teorUpper.append(math.exp(-_lambda * numOfSF[i] / numOfSeeds * t_23ms[i]))
    # y_teorUpper.append(math.exp(-_lambda * point[0] * t_23ms[i]))

print("teor prob up bound: ")
print(y_teorUpper[::-1])

y_teorLower = []
for i in range(len(t_23ms)):
    y_teorLower.append(math.exp(-2 * _lambda * numOfSF[i] / numOfSeeds * t_23ms[i]))
    # y_teorLower.append(math.exp(-2 * _lambda * point[0] * t_23ms[i]))

print("teor prob low bound: ")
print(y_teorLower[::-1])


print()
kmax = 5
PDRTeorLOW = 0
PDRTeorUP = 0
N = point[0]
for i in range(kmax+1):
    ni = numOfSF[i] / numOfSeeds
    PDRTeorLOW += (ni*math.exp(-2 * _lambda * ni * t_23ms[i]))/N
    PDRTeorUP += (ni*math.exp(-1 * _lambda * ni * t_23ms[i]))/N

print("Teor PDR low = {}".format(PDRTeorLOW))
print("Teor PDR up = {}".format(PDRTeorUP))
print()


x = ["7","8","9","10","11","12"]

plt.plot(x, resOfModelingProbForSF[::-1],  color="purple", marker='o',  label = "Результы моделирования")
plt.plot(x, y_teorUpper[::-1],  color="b", linestyle="dashed", label = "Верхняя граница")
plt.plot(x, y_teorLower[::-1], color="r", linestyle="dashed", label="Нижняя граница")


plt.xlabel("SF")
plt.ylabel("Вероятность доставки")
plt.grid()
plt.legend()
plt.savefig("RES_OF_MODELING.png")
plt.show()






