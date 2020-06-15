#!/usr/bin/env python3

import datetime
from sys import argv
from glob import glob
import os

from matplotlib import pyplot as plt


csvs = argv[1:] if len(argv) > 1 else sorted(glob(os.path.dirname(os.path.realpath(__file__))+'/data/*.csv'))

head = []
unit = []
data = [[], [], [], [], []]


def head_line(line, rm_chrs=["#", " ", "\n"], sep=","):
    global head
    if head != []:
        return
    for rm_chr in rm_chrs:
        line = line.replace(rm_chr, "")
    head = line.split(sep)


def unit_line(line, rm_chrs=["#", " ", "\n"], sep=","):
    global unit
    if unit != []:
        return
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
    for i in range(1, 5):
        data[i].append(float(sep_line[i]))


for csv in csvs:
    with open(csv, "r") as f:
        head_line(f.readline())
        unit_line(f.readline())
        for line in f.readlines():
            data_line(line)


# data[i], i =
# 0 : time
# 1 : temperature(outside)
# 2 : temperature(inside)
# 3 : pressure(inside)
# 4 : humidity(inside)

fig, ax1 = plt.subplots(sharex=True)
ax1.set_xlabel("time")
ax1.tick_params(axis="x", rotation=45)
ax1.set_ylabel('°C')
ax1.plot(data[0], data[2], color='tab:blue', label='inside')
ax1.plot(data[0], data[1], color='tab:red', label='outside')
ax1.legend(frameon=False)
plt.show()

# fig, ax1 = plt.subplots(sharex=True)
# ax1.set_xlabel("time")
# ax1.tick_params(axis="x", rotation=45)
# left = 2
# right = 4
# ax1.set_ylabel(unit[left])
# ax1.plot(data[0], data[left], color="tab:red", label=head[left])
# ax1.legend(loc="upper left", bbox_to_anchor=(0, 1.1), frameon=False)
# ax2 = ax1.twinx()
# ax2.set_ylabel(unit[right])
# ax2.plot(data[0], data[right], color="tab:blue", label=head[right])
# ax2.legend(loc="upper right", bbox_to_anchor=(1, 1.1), frameon=False)
# plt.show()
