'''
Script to plot results of our experiments.
'''

from matplotlib import pyplot as plt

generations = range(1, 21)
errors1 = [ 97.8744310971,
            90.3661240419,
            77.8403112608,
            69.6869406571,
            66.4484880416,
            66.2994756253,
            66.2994756253,
            66.2994756253,
            65.4913779099,
            63.8015407621,
            63.2180512569,
            63.2136213008,
            62.9868357819,
            50.1069339293,
            30.6602920676,
            15.3422795504,
            11.0198406518,
            9.17610129941,
            1.51324265618e-14,0]

errors2 = [94.8936532896,
72.1905151233,
69.6328708096,
68.9711415785,
68.9711415785,
68.501554306,
57.1375379793,
37.9398735248,
34.6370497597,
 19.9283831167,
 8.52025880547,
 8.52025880547,
 7.2424751896,
 3.6212375948,
 3.6212375948,
 3.6212375948,
 3.6212375948,
 3.6212375948,
 3.6212375948,
 1.3370814872e-14]

# errors2 = [102.149671868,
# 89.5210529639,
# 88.9546129119,
# 85.2248345628,
# 83.7863805878,
# 83.7863805878,
# 82.4943960298,
# 82.4943960298,
# 76.8860087373,
#  69.0011376841,
#  63.7210172497,
#  60.0408303037,
#  60.0408303037,
#  60.0408303037,
#  49.3716579275,
#  49.3716579275,
#  49.3716579275,
#  49.3716579275,
#  49.3716579275,
#  46.6940352104,
#  46.0807534031,
#  37.1795050484,
#  32.6502520645,
#  25.0437690665,
#  24.9934730957,
#  21.896397474,
#  20.7098941781,
#  20.3391196485,
#  19.7134842549,
#  18.934260312,
#  18.6108098615,
#  18.6108098615,
#  17.3626835422,
#  17.1656187969,
#  17.1656187969]

# errors3 = [97.5771946309,
# 81.3045954347,
# 72.3634462444,
# 65.3291645325,
# 63.2644933559,
# 63.2644933559,
# 61.5186274553,
# 60.6808714904,
# 60.1424542679,
#  60.1424542679,
#  60.1424542679,
#  60.1424542679,
#  60.0493520215,
#  60.0493520215,
#  44.3464123994,
#  43.6890078125,
#  38.0645822562,
#  34.3149541071,
#  9.72017212283,
#  9.72017212283,
#  9.72017212283,
#  9.72017212283,
#  9.72017212283,
#  9.72017212283,
#  9.72017212283,
#  9.72017212283,
#  9.72017212283,
#  9.72017212283,
#  9.72017212283,
#  9.72017212283,
#  9.72017212283,
#  9.72017212283,
#  9.72017212283,
#  9.72017212283,
#  9.72017212283]

# errors4 = [88.5549569363,
# 88.5549569363,
# 73.9552684806,
# 71.3003262588,
# 71.3003262588,
# 71.3003262588,
# 71.3003262588,
# 70.1532954873,
# 70.1532954873,
# 70.1532954873,
# 70.0030126532,
# 70.0030126532,
# 70.0030126532,
# 70.0030126532,
# 70.0030126532,
# 67.3072245512,
# 65.0896263998,
# 65.0896263998,
# 65.0896263998,
# 55.3243182764,
# 55.3243182764,
# 55.3243182764,
# 55.3243182764,
# 55.3243182764,
# 55.3243182764,
# 55.3243182764,
# 55.3243182764,
# 55.3243182764,
# 55.3243182764,
# 55.3243182764,
# 55.3243182764,
# 55.3243182764,
# 55.3243182764,
# 55.3243182764,
# 55.3243182764]

# errors5 = [98.5061267661,
# 98.5061267661,
# 83.5537568376,
# 82.2208141577,
# 81.5057231944,
# 79.3871523424,
# 76.8383895069,
# 75.9853644713,
# 75.0145251304,
# 74.7514564926,
# 74.7514564926,
# 74.619229358,
# 74.619229358,
# 74.619229358,
# 74.619229358,
# 74.619229358,
# 74.619229358,
# 74.619229358,
# 74.619229358,
# 74.619229358,
# 74.619229358,
# 74.619229358,
# 73.1701667322,
# 72.7121123278,
# 72.2560221602,
# 70.7523777933,
# 70.7523777933,
# 70.5632480013,
# 70.5632480013,
# 70.5632480013,
# 70.5632480013,
# 70.5632480013,
# 70.5632480013,
# 70.5632480013,
# 70.5632480013]

plt.plot(generations, errors1, 's', label='Trial 1')
plt.plot(generations, errors2, '^', label='Trial 2')
plt.title('Error Over Time', {'fontsize': 40})

legend = plt.legend(loc='upper right', shadow=False)

plt.xlabel('Generation')
plt.ylabel('Error')
plt.show()