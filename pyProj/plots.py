import matplotlib.pyplot as plt
import math
import pandas as pd


# Build plots for SF

# x = ["7","8","9","10","11","12"]
# resOfModelingProbForSFWithOptimization = [0.9193263333333325, 0.8871229999999986, 0.8192256666666663, 0.8273063333333326, 0.8260176666666667, 0.8265659999999987]
# y_teorUpperWithOptimization = [0.9326539940743108, 0.9318996267963604, 0.8458609736166407, 0.8463599813581162, 0.845857533789009, 0.8453157946180059]
# y_teorLowerWithOptimization = [0.8698434726627645, 0.8684369144231958, 0.7154807866876913, 0.7163252180445109, 0.7154749674676244, 0.7145587926306707]
#
#
# resOfModelingProbForSFWithoutOptimization =[0.9195126666666656, 0.8878883333333334, 0.7990060000000005, 0.7745826666666656, 0.0, 0.0]
# y_teorUpperWithoutOptimization = [0.9326539940743108, 0.9318996267963604, 0.8263585387698734, 0.7849116358488841, 1.0, 1.0]
# y_teorLowerWithoutOptimization = [0.8698434726627645, 0.8684369144231958, 0.6828684345978804, 0.6160862760909713, 1.0, 1.0]
#
# plt.plot(x, resOfModelingProbForSFWithOptimization,  color="purple", marker='o',  label = "modeling with optimization")
# plt.plot(x, y_teorUpperWithOptimization,  color="b", linestyle="dashed", label = "upper bound with optimization")
# plt.plot(x, y_teorLowerWithOptimization, color="r", linestyle="dashed", label="lower bound with optimization")
#
# plt.plot(x, resOfModelingProbForSFWithoutOptimization,  color="green", marker='o',  label = "modeling without optimization")
# plt.plot(x, y_teorUpperWithoutOptimization,  color="black", linestyle="dashed", label = "upper bound without optimization")
# plt.plot(x, y_teorLowerWithoutOptimization, color="orange", linestyle="dashed", label="lower bound without optimization")
#
#
# plt.xlabel("SF")
# plt.ylabel("Вероятность доставки")
# plt.grid()
# plt.legend()
# plt.savefig("RES_OF_MODELING.png")
# plt.show()









if (False):

    # Build plots fix Radius

    fName = "/dope/forStudy/ns-3/resultOfmodeling/table.csv"
    file = pd.read_csv(fName, header = None)


    fixRadius = 3000
    PDR = {}
    PDR_upper = {}
    PDR_lower = {}
    countExperements = {}

    for i in range(len(file[0])-1):
        if int(file[1][i+1]) == fixRadius:
            if PDR.get(int(file[0][i+1])) == None:
                PDR[int(file[0][i + 1])] = float(file[12][i + 1].replace(',','.'))
                PDR_upper[int(file[0][i + 1])] = float(file[13][i + 1].replace(',','.'))
                PDR_lower[int(file[0][i + 1])] = float(file[14][i + 1].replace(',','.'))
                countExperements[int(file[0][i + 1])] = 1
            else:
                PDR[int(file[0][i+1])] += float(file[12][i+1].replace(',','.'))
                PDR_upper[int(file[0][i+1])] += float(file[13][i+1].replace(',','.'))
                PDR_lower[int(file[0][i+1])] += float(file[14][i+1].replace(',','.'))
                countExperements[int(file[0][i+1])] += 1

    print(PDR)
    print(countExperements)
    PDR_list = []
    PDR_list_upper = []
    PDR_list_lower = []

    for i in sorted(countExperements.keys()):
        PDR_list.append(PDR[i] / countExperements[i])
        PDR_list_upper.append(PDR_upper[i] / countExperements[i])
        PDR_list_lower.append(PDR_lower[i] / countExperements[i])


    print(PDR_list)

    plt.plot(sorted(countExperements.keys()), PDR_list,  color="green", marker='o',  label = "modeling ")
    plt.plot(sorted(countExperements.keys()), PDR_list_upper,  color="black", linestyle="dashed", label = "upper bound ")
    plt.plot(sorted(countExperements.keys()), PDR_list_lower, color="orange", linestyle="dashed", label="lower bound ")
    #
    #
    plt.xlabel("NumOfDevices")
    plt.ylabel("PDR")
    plt.grid()
    plt.legend()
    plt.savefig("resultOfmodeling/fix{}R.png".format(fixRadius))
    plt.show()

else:
    # Build plots fix numOfDevices

    fName = "/dope/forStudy/ns-3/resultOfmodeling/table.csv"
    file = pd.read_csv(fName, header = None)


    fixNumOfDevices = 3000
    PDR = {}
    PDR_upper = {}
    PDR_lower = {}
    countExperements = {}

    for i in range(len(file[0])-1):
        if int(file[0][i+1]) == fixNumOfDevices:
            if PDR.get(int(file[1][i+1])) == None:
                PDR[int(file[1][i + 1])] = float(file[12][i + 1].replace(',','.'))
                PDR_upper[int(file[1][i + 1])] = float(file[13][i + 1].replace(',','.'))
                PDR_lower[int(file[1][i + 1])] = float(file[14][i + 1].replace(',','.'))
                countExperements[int(file[1][i + 1])] = 1
            else:
                PDR[int(file[1][i+1])] += float(file[12][i+1].replace(',','.'))
                PDR_upper[int(file[1][i+1])] += float(file[13][i+1].replace(',','.'))
                PDR_lower[int(file[1][i+1])] += float(file[14][i+1].replace(',','.'))
                countExperements[int(file[1][i+1])] += 1

    print(PDR)
    print(countExperements)
    PDR_list = []
    PDR_list_upper = []
    PDR_list_lower = []

    for i in sorted(countExperements.keys()):
        PDR_list.append(PDR[i] / countExperements[i])
        PDR_list_upper.append(PDR_upper[i] / countExperements[i])
        PDR_list_lower.append(PDR_lower[i] / countExperements[i])


    print(PDR_list)

    plt.plot(sorted(countExperements.keys()), PDR_list,  color="green", marker='o',  label = "modeling ")
    plt.plot(sorted(countExperements.keys()), PDR_list_upper,  color="black", linestyle="dashed", label = "upper bound ")
    plt.plot(sorted(countExperements.keys()), PDR_list_lower, color="orange", linestyle="dashed", label="lower bound ")
    #
    #
    plt.xlabel("Radius")
    plt.ylabel("PDR")
    plt.grid()
    plt.legend()
    plt.savefig("resultOfmodeling/fix{}ED.png".format(fixNumOfDevices))
    plt.show()