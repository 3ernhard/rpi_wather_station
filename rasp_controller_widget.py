#!/usr/bin/env python3

import datetime
from glob import glob
import os

# use all csv files in ./data/
csvs = sorted(glob(os.path.dirname(os.path.realpath(__file__))+'/data/*.csv'))

head = []
unit = []
data = [[], [], [], []]


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
    for i in range(1, len(data)):
        data[i].append(float(sep_line[i]))


def print_result(n, s):
    print(fr"<result{n:d}>{s}</result{n:d}>")


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

print_result(1, data[0][-1].strftime("%H:%M"))
print_result(2, data[1][-1])
print_result(3, data[2][-1])
print_result(4, data[3][-1])
