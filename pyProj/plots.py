import matplotlib.pyplot as plt
import math



x = ["7","8","9","10","11","12"]
# t_23ms = [1.48275, 0.8233, 0.37069, 0.20582, 0.11315, 0.0617]
# kmin = 0
# kmax = 5
# niWithoutOPT = [0, 0, 0, 0, 0, 1000]
# niWithOPT = [20, 35, 78, 141, 256 ,470]
# _lambda = 1 / 300
# N = 1000
#
# PDRWithOPTLow = 0
# PDRWithOPTUp = 0
# PDRWithoutOPTLow = 0
# PDRWithoutOPTUp = 0
# for i in range(kmax+1):
#     PDRWithOPTLow += (niWithOPT[i]*math.exp(-2 * _lambda * niWithOPT[i] * t_23ms[i]))/N
#     PDRWithOPTUp += (niWithOPT[i]*math.exp(-1 * _lambda * niWithOPT[i] * t_23ms[i]))/N
#     PDRWithoutOPTUp += (niWithoutOPT[i]*math.exp(-1 * _lambda * niWithoutOPT[i] * t_23ms[i]))/N
#     PDRWithoutOPTLow += (niWithoutOPT[i]*math.exp(-2 * _lambda * niWithoutOPT[i] * t_23ms[i]))/N
#
# print("PDRWithOPTUp " + str(PDRWithOPTUp))
# print("PDRWithOPTLow " + str(PDRWithOPTLow))
# print("PDRWithoutOPTUp " + str(PDRWithoutOPTUp))
# print("PDRWithoutOPTLow " + str(PDRWithoutOPTLow))

#
#
resOfModelingProbForSFWithOptimization = [0.9193263333333325, 0.8871229999999986, 0.8192256666666663, 0.8273063333333326, 0.8260176666666667, 0.8265659999999987]
y_teorUpperWithOptimization = [0.9326539940743108, 0.9318996267963604, 0.8458609736166407, 0.8463599813581162, 0.845857533789009, 0.8453157946180059]
y_teorLowerWithOptimization = [0.8698434726627645, 0.8684369144231958, 0.7154807866876913, 0.7163252180445109, 0.7154749674676244, 0.7145587926306707]


resOfModelingProbForSFWithoutOptimization =[0.9195126666666656, 0.8878883333333334, 0.7990060000000005, 0.7745826666666656, 0.0, 0.0]
y_teorUpperWithoutOptimization = [0.9326539940743108, 0.9318996267963604, 0.8263585387698734, 0.7849116358488841, 1.0, 1.0]
y_teorLowerWithoutOptimization = [0.8698434726627645, 0.8684369144231958, 0.6828684345978804, 0.6160862760909713, 1.0, 1.0]

plt.plot(x, resOfModelingProbForSFWithOptimization,  color="purple", marker='o',  label = "modeling with optimization")
plt.plot(x, y_teorUpperWithOptimization,  color="b", linestyle="dashed", label = "upper bound with optimization")
plt.plot(x, y_teorLowerWithOptimization, color="r", linestyle="dashed", label="lower bound with optimization")

plt.plot(x, resOfModelingProbForSFWithoutOptimization,  color="green", marker='o',  label = "modeling without optimization")
plt.plot(x, y_teorUpperWithoutOptimization,  color="black", linestyle="dashed", label = "upper bound without optimization")
plt.plot(x, y_teorLowerWithoutOptimization, color="orange", linestyle="dashed", label="lower bound without optimization")


plt.xlabel("SF")
plt.ylabel("Вероятность доставки")
plt.grid()
plt.legend()
plt.savefig("RES_OF_MODELING.png")
plt.show()