#!/usr/bin/env python3

import datetime
from sys import argv

from matplotlib import pyplot as plt

csv = argv[1]

head = []
unit = []
data = [[], [], [], []]


def head_line(line, rm_chrs=["#", " ", "\n"], sep=","):
    global head
    for rm_chr in rm_chrs:
        line = line.replace(rm_chr, "")
    head = line.split(sep)


def unit_line(line, rm_chrs=["#", " ", "\n"], sep=","):
    global unit
    for rm_chr in rm_chrs:
        line = line.replace(rm_chr, "")
    unit = line.split(sep)


def data_line(line, rm_chrs=[" ", "\n"], sep=",", comment="#"):
    global unit, data
    if len(line) == 0 or line[0] == comment:
        return
    for rm_chr in rm_chrs:
        line = line.replace(rm_chr, "")
    sep_line = line.split(sep)
    data[0].append(datetime.datetime.strptime(sep_line[0], unit[0]))
    data[1].append(float(sep_line[1]))
    data[2].append(float(sep_line[2]))
    data[3].append(float(sep_line[3]))


with open(csv, "r") as f:
    head_line(f.readline())
    unit_line(f.readline())
    for line in f.readlines():
        data_line(line)


# data[i], i =
# 0 : time
# 1 : temperature
# 2 : pressure
# 3 : humidity

fig, ax1 = plt.subplots(sharex=True)
ax1.set_xlabel("time")
ax1.tick_params(axis="x", rotation=45)

ax1.set_ylabel(unit[1])
ax1.plot(data[0], data[1], color="tab:red", label="temperature")
ax1.legend(loc="upper left", bbox_to_anchor=(0, 1.1), frameon=False)

ax2 = ax1.twinx()
ax2.set_ylabel(unit[3])
ax2.plot(data[0], data[3], color="tab:blue", label="humidity")
ax2.legend(loc="upper right", bbox_to_anchor=(1, 1.1), frameon=False)

plt.show()
