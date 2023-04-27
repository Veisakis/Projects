import re
from io import StringIO

import pandas as pd
import matplotlib.pyplot as plt

def nodeName(n):
    return str(n) + "SA"

FILEPATH = r"C:\Users\mveis\Desktop\results.txt"

START_SENTENCE = "Bus              Phasor       Angle in                Real           Imaginary"
END_SENTENCE = "Memory storage figures for the preceding"

NUMBER_OF_NODES = 27
NODES_NAMES = list(map(nodeName, range(NUMBER_OF_NODES)))
NODES_POSITION = [x * 100 for x in range(NUMBER_OF_NODES)]

START_INDEX = 0
END_INDEX = 0

with open(FILEPATH, "r") as f:
    lines = f.readlines()

text = []
for line in lines:
    if START_SENTENCE in line:
        START_INDEX = 1
        continue

    if END_SENTENCE in line:
        END_INDEX = 1
        continue
    
    if (START_INDEX == 1) and (END_INDEX == 0):
        if line == "\n":
            continue
        text.append(line)

    if (START_INDEX == 1) and (END_INDEX == 1):
        break

data = []
for line in text:
    line = re.sub("\s+", ",", line.strip())
    data.append(line)

data_str = "\n".join(data)
data_file = StringIO(data_str)

df = pd.read_csv(data_file)

V_she = []
for nd in NODES_NAMES:
    series = df.loc[df["name"] == nd]
    V_she.append(series["magnitude"].values[0])

# I_she = []
# for nd in NODES_NAMES:
#     series = df.loc[ (df["Node-K"] == nd) | (df["Node-M"] == nd)]
#     I_she.append(series["I-magn"].values[0])

plt.style.use('classic')
plt.plot(NODES_POSITION, V_she)

plt.xlabel("Distance [m]")
plt.ylabel("Voltage [V]")
plt.title("Voltage in the Cable's Sheath")

plt.grid(True)
plt.show()

