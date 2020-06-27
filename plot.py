#!/usr/bin/env python3

import datetime
from sys import argv
from glob import glob
import os

import numpy as np
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
    global data
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
            try:
                data_line(line)
            except ValueError:
                print(f"Invalid data line in '{csv}' detected.")
                continue


# data[i], i =
# 0 : time
# 1 : temperature(outside)
# 2 : temperature(inside)
# 3 : pressure(inside)
# 4 : humidity(inside)

t_in_mean = np.mean(data[2])
t_out_mean = np.mean(data[1])

t_in_str =  f'inside:  {data[2][-1]:.1f} <{t_in_mean:.1f}> °C'
t_out_str = f'outside: {data[1][-1]:.1f} <{t_out_mean:.1f}> °C' 

fig, ax1 = plt.subplots(sharex=True)
ax1.set_xlabel("time")
ax1.tick_params(axis="x", rotation=45)
ax1.set_ylabel('°C')
ax1.plot(data[0], data[2], color='tab:blue', label=t_in_str)
ax1.plot(data[0], data[1], color='tab:red', label=t_out_str)
ax1.axhline(t_in_mean, color='tab:blue', zorder=0)
ax1.axhline(t_out_mean, color='tab:red', zorder=0)
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
