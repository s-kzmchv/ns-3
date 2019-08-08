import matplotlib.pyplot as plt
import math



x = ["7","8","9","10","11","12"]
t_23ms = [1.48275, 0.8233, 0.37069, 0.20582, 0.11315, 0.0617]
kmin = 0
kmax = 5
niWithoutOPT = [0, 0, 0, 0, 0, 1000]
niWithOPT = [20, 35, 78, 141, 256 ,470]
_lambda = 1 / 300
N = 1000

PDRWithOPTLow = 0
PDRWithOPTUp = 0
PDRWithoutOPTLow = 0
PDRWithoutOPTUp = 0
for i in range(kmax+1):
    PDRWithOPTLow += (niWithOPT[i]*math.exp(-2 * _lambda * niWithOPT[i] * t_23ms[i]))/N
    PDRWithOPTUp += (niWithOPT[i]*math.exp(-1 * _lambda * niWithOPT[i] * t_23ms[i]))/N
    PDRWithoutOPTUp += (niWithoutOPT[i]*math.exp(-1 * _lambda * niWithoutOPT[i] * t_23ms[i]))/N
    PDRWithoutOPTLow += (niWithoutOPT[i]*math.exp(-2 * _lambda * niWithoutOPT[i] * t_23ms[i]))/N

print("PDRWithOPTUp " + str(PDRWithOPTUp))
print("PDRWithOPTLow " + str(PDRWithOPTLow))
print("PDRWithoutOPTUp " + str(PDRWithoutOPTUp))
print("PDRWithoutOPTLow " + str(PDRWithoutOPTLow))

#
#
# resOfModelingProbForSFWithOptimization = [0.9891319999999999, 0.9895919999999999, 0.9545600000000001, 0.881876, 0.7060040000000001, 0.172408]
# y_teorUpperWithOptimization = [0.9909914886534971, 0.9842838087396947, 0.9609894322728209, 0.8881445213181817, 0.6717101651655655, 0.04785223278492157]
# y_teorLowerWithOptimization = [0.9820641305836741, 0.9688146161471197, 0.9235006889400386, 0.7888006907475019, 0.4511945459867513, 0.0022898361825023222]
#
#
# resOfModelingProbForSFWithoutOptimization =[0.9764400000000001, 0.9675640000000001, 0.9328839999999998, 0.8592920000000003, 0.6813519999999998, 0.17597200000000005]
# y_teorUpperWithoutOptimization = [0.9810547603761872, 0.9861417552938195, 0.9537643982844155, 0.8739920204105434, 0.6499496807412428, 0.07105951596858905]
# y_teorLowerWithoutOptimization = [0.962468442856778, 0.9724755615339755, 0.9096665274348332, 0.7638620517413036, 0.42243458749564344, 0.005049454809690162]
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