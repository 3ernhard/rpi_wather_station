#!/usr/bin/env python3

import datetime
from sys import argv
from glob import glob
import os

import numpy as np
from matplotlib import pyplot as plt

# Plot all csv files in ./data/ if no argument is passed, else plot the passed csv file.
csvs = argv[1:] if len(argv) > 1 else sorted(glob(os.path.dirname(os.path.realpath(__file__))+'/data/????-??-??T??-??-??.csv'))

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

mean_in_temp = np.mean(data[2])
mean_out_temp = np.mean(data[1])

if 1:

    plt.title(data[0][-1].strftime("%d. %b, %H:%M"))
    plt.ylabel('°C')
    plt.xlim((data[0][0], data[0][-1]))
    plt.plot(data[0], data[2], color='tab:blue', label=f'inside:  {data[2][-1]:.1f} <{mean_in_temp:.1f}> °C')
    plt.plot(data[0], data[1], color='tab:red', label=f'outside: {data[1][-1]:.1f} <{mean_out_temp:.1f}> °C')
    plt.axhline(mean_out_temp, color='black', zorder=0)
    plt.tick_params(axis="x", rotation=45)
    plt.legend(frameon=False)


else:

    mean_in_hum = np.mean(data[4])

    fig, (ax1, ax2) = plt.subplots(2)

    ax1.set(title=data[0][-1].strftime("%d. %b, %H:%M"))
    ax1.set(ylabel='°C')
    ax1.set(xlim=(data[0][0], data[0][-1]))
    ax1.plot(data[0], data[2], color='tab:blue', label=f'inside:  {data[2][-1]:.1f} <{mean_in_temp:.1f}> °C')
    ax1.plot(data[0], data[1], color='tab:red', label=f'outside: {data[1][-1]:.1f} <{mean_out_temp:.1f}> °C')
    ax1.axhline(mean_out_temp, color='black', zorder=0)
    ax1.tick_params(axis="x", rotation=45)
    ax1.legend(frameon=False)
    
    ax2.set(ylabel='%')
    ax2.set(xlim=(data[0][0], data[0][-1]))
    ax2.set(ylim=(0, 100))
    ax2.plot(data[0], data[4], color='tab:blue', label=f'inside: {data[4][-1]:.1f} <{mean_in_hum:.1f}> %')
    ax2.axhline(mean_in_hum, color='black', zorder=0)
    ax2.tick_params(axis="x", rotation=45)
    ax2.legend(frameon=False)


plt.show()
