FILEPATH = r"C:\Users\mveis\Desktop\circuit.txt"
X_DIST = [0, 1, 2, 3]

NODE_CONDUCTOR = ["1A", "2A", "3A", "4A"]
NODE_SHEATH = ["1SA", "2SA", "3SA", "4SA"]

import re
from io import StringIO

import pandas as pd
import matplotlib.pyplot as plt


START_SENTENCE = "Output for steady-state phasor switch currents."
END_SENTENCE = "Solution at nodes with known voltage."

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

I_con = []
for node in NODE_CONDUCTOR:
    series = df.loc[ (df["Node-K"] == node) | (df["Node-M"] == node)]
    I_con.append(series["I-magn"].values[0])

I_she = []
for node in NODE_SHEATH:
    series = df.loc[ (df["Node-K"] == node) | (df["Node-M"] == node)]
    I_she.append(series["I-magn"].values[0])


plt.style.use('classic')
plt.plot(X_DIST, I_she)

plt.xlabel("Distance [km]")
plt.ylabel("Current [A]")
plt.title("Induced Current in the Cable Sheath")

plt.grid(True)
plt.show()

