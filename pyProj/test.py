import datetime
import time
import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt


# print(3135962004 + 0xFFFFFFFF)
#
#
# print(
#     datetime.datetime.fromtimestamp(
#         3135962004 - 5000
#     ).strftime('%Y-%m-%d %H:%M:%S')
# )



# Мой способ который считает число пакетов учавствовавших в колизии и соответсвенно не переданных
tmpName = ""
for file in os.listdir("/dope/forStudy/diplom/ns-3-dev-git-lorawan/tmp/"):
    if file.endswith("nodes.csv"):
        print(file)
        tmpName = file
        break

fName = "/dope/forStudy/diplom/ns-3-dev-git-lorawan/tmp/" + tmpName

tmp = pd.read_csv(fName, header = None)
valueTime = tmp[0].values
#
# counter = 0
# counterD = 0
#
# for i in range(len(valueTime) - 1):
#     if i == 0:
#         continue
#     if float(valueTime[i+1]) - float(valueTime[i]) < 0.12314:
#         print(valueTime[i+1])
#         counter += 1
#         if float(valueTime[i])- float(valueTime[i-1]) > 0.12314:
#             counterD += 1
# print(counter)
# print(counterD)
#
#
#
#
# # Мой способ по файлу но имитирует как в НС3
# # fName = "/dope/forStudy/diplom/ns-3-dev-git-lorawan/tmp/myTest-1557905394-0-trace-ed-msgs.csv"
# #
# # tmp = pd.read_csv(fName, header = None)
# # valueTime = tmp[0].values
#
# counter = 0
# counterDestr = 0
#
# collisionWith = -1
#
# for i in range(len(valueTime) - 1):
#     if i == 0:
#         continue
#     if collisionWith == -1:
#         if float(valueTime[i+1]) - float(valueTime[i]) < 0.11802:
#             print(valueTime[i+1])
#             counter += 1
#             collisionWith = float(valueTime[i])
#             counterDestr +=1
#     else:
#         if  float(valueTime[i+1]) - collisionWith < 0.11802:
#             print(valueTime[i+1])
#             counter += 1
#         else:
#             collisionWith = -1
#
# print(counter)
# print(counterDestr)











# Сравнения непереданных пакетов которые полученны моим способом и моделированием
# fName = "testTime.csv"
#
# tmp = pd.read_csv(fName, header = None)
# valueTimeMY = tmp[0].values
# valueTimeTheir = tmp[1].values
#
# counterMY = 0
# counterTheir = 0
#
# counterRepeat = 0
#
# while (counterMY != len(valueTimeMY) and counterTheir != len(valueTimeTheir)):
#
#     if float(valueTimeTheir[counterTheir]) == float(valueTimeTheir[counterTheir-1]):
#         counterTheir += 1
#         counterRepeat += 1
#
#     if abs(float(valueTimeMY[counterMY]) - float(valueTimeTheir[counterTheir])) < 0.01:
#         print(valueTimeMY[counterMY], '\t', valueTimeTheir[counterTheir])
#         counterMY += 1
#         counterTheir += 1
#     else:
#         print(valueTimeMY[counterMY], '\t')
#         counterMY += 1
#
# print('\n', str(counterRepeat))




# Подсчет числа повторений по значениям времени
# fName = "testTime.csv"
#
# tmp = pd.read_csv(fName, header = None)
# valueTimeTheir = tmp[3].values
#
# counterRepeat = 0
#
# for i in range(len(valueTimeTheir) - 1):
#     if float(valueTimeTheir[i+1]) == float(valueTimeTheir[i]):
#         # print(valueTimeTheir[i+1])
#         counterRepeat += 1
#     else:
#         print(valueTimeTheir[i])
#         counterRepeat += 0
#
#
#
# print('\n', str(counterRepeat))
# print(len(valueTimeTheir))




# Подсчет числа повторений по значениям пакетов
# fName = "testTime.csv"
#
# tmp = pd.read_csv(fName, header = None)
# valuePackets = tmp[5].values
# valueTime = tmp[3].values
#
# counterRepeat = 0
# packets = set()
#
# for value in valuePackets:
#     packets.add(value)
#
#
# print(packets)
# print(len(packets))


# Подсчет ??????
# fNameFull = "/dope/forStudy/diplom/ns-3-dev-git-lorawan/tmp/myTest-1557647585-0-trace-ed-msgs.csv"
# fNameNS = "/dope/forStudy/diplom/ns-3-dev-git-lorawan/tmp/myTest-1557647585-0-trace-ns-dsmsgs.csv"
#
#
# tmpFull = pd.read_csv(fNameFull, header = None)
# tmpNS = pd.read_csv(fNameNS, header = None)
#
# idDevicePacketFull = tmpFull[2].values
# idDevicePacketNS = tmpNS[2].values
#
# timePacketFull = tmpFull[0].values
#
# res = []
#
# for i in range(len(idDevicePacketFull)):
#     if idDevicePacketFull[i] not in idDevicePacketNS:
#         print(timePacketFull[i])
#         res.append(timePacketFull[i])
#
#
# print(len(res))




# Подсчет сравнение значени непринятых значений из файла и из вхождений без повторений
# fName = "testTime.csv"
#
# tmp = pd.read_csv(fName, header = None)
# valueTimeNS = tmp[7].values
# valueTimeWithOutRep = tmp[8].values
#
# counterNS = 0
# counterRep = 0
#
# notFindNS = []
# notFindRep = []
# print(len(valueTimeNS))
# print(len(valueTimeWithOutRep))
#
#
# while (counterNS != 270 and counterRep != 270):
#     if abs(float(valueTimeNS[counterNS]) - float(valueTimeWithOutRep[counterRep])) < 0.001:
#         # print(valueTimeMY[counterMY], '\t', valueTimeTheir[counterTheir])
#         counterNS += 1
#         counterRep += 1
#     else:
#         if float(valueTimeNS[counterNS]) < float(valueTimeWithOutRep[counterRep]):
#             notFindNS.append(float(valueTimeNS[counterNS]))
#             counterNS += 1
#         else:
#             notFindRep.append(float(valueTimeWithOutRep[counterRep]))
#             counterRep += 1
#
# print(notFindNS)
# print(notFindRep)






# ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
# fName = "testTime.csv"
#
# tmp = pd.read_csv(fName, header = None)
# valueTimeWithOutRep = tmp[7].values
# valueTimeMY= tmp[8].values
#
# tmp = []
#
# for value in valueTimeMY:
#     for value2 in valueTimeWithOutRep:
#
#         if value - value2 < 0.001:
#             tmp.append(value)
#             break
#
# for value in valueTimeMY:
#     if value not in tmp:
#         print(value)