from pathlib import Path
from matplotlib import pyplot as plt

skiplines = 2 #Change based on the raw data file format

def getData(filename):
    strength, odor, secs = [], [], 0

    with open(filename, "r") as f:
        data = f.readlines()[skiplines:]

    for row in data:
        strength.append(float(row.split(",")[0]))
        odor.append(float(".".join(row.split(",")[1:])))
        secs += 1

    return strength, odor, range(secs)

def plotGraph(x, y1, y2, filename, directory):
    plt.style.use("bmh")

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.plot(x, y1, color='black', label="Strength")
    ax2.plot(x, y2, color='firebrick', label="Odor Intensity")

    ax1.legend(loc="lower right")
    ax2.legend(loc="upper right")

    ax1.set_title(filename, fontsize="xx-large")
    ax1.set_xlabel("Time (sec)")
    ax1.set_ylabel("Strength")
    ax2.set_ylabel("Odor Intensity")

    ax1.set_xticks(x) 
    ax1.set_xlim(0, max(x))
    ax1.set_ylim(0,1000)
    ax2.set_ylim(0,5)

    ax2.grid(which='major', alpha=1.0)

    path = directory / filename
    plt.savefig(path, format="png")
    plt.show()

def main():
    img_dir = Path("img")
    img_dir.mkdir(exist_ok=True)

    for file in Path('data').iterdir():
        strength, odor, time = getData(file)
        plotGraph(time, strength, odor, file.stem, img_dir)

if __name__ == "__main__":
    main()
