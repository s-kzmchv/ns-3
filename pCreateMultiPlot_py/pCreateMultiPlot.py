import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import argparse

def parseFileInfo(s):
    r = s.split('|')
    n = len(r)
    fName = ''
    fLabel = ''
    lineStyle = ''
    if n == 0:
        raise Exception('file string is incorrect')
    fName = r[0]
    fLabel = fName
    if n > 1:
        fLabel = r[1]
        if n > 2:
            lineStyle = r[2]
    return (fName, fLabel, lineStyle)

parser = argparse.ArgumentParser(description = 'The simple script building plots')
parser.add_argument("--logx", help = 'use log scale x axis', action = 'store_true')
parser.add_argument("--logy", help = 'use log scale y axis', action = 'store_true')
parser.add_argument("--grid", help = 'print grid', action = 'store_true')
parser.add_argument("--xlabel", help = 'x label', default = '')
parser.add_argument("--ylabel", help = 'y label', default = '')
parser.add_argument("--xticks", help = 'use x values as ticks', action = 'store_true')
parser.add_argument("--yticks", help = 'use x values as ticks', action = 'store_true')
parser.add_argument("files", help = 'strings containing file name and additional parameters', nargs = '*')
args = parser.parse_args(sys.argv[1:])

if len(args.files) == 0:
    raise Exception('files have not been found')

xvalues = set()
yvalues = set()
for s in args.files:
    fName, fLabel, lineStyle = parseFileInfo(s)
    d = pd.read_csv(fName, header = None)
    print('file \'{}\' has been loaded'.format(fName))
    plt.plot(d[0], d[1], lineStyle, label = fLabel)
    xvalues.update(d[0].values)
    yvalues.update(d[1].values)
    
xvalues = list(xvalues)
yvalues = list(yvalues)

plt.xlabel(args.xlabel)
plt.ylabel(args.ylabel)
plt.grid(args.grid)
plt.legend()
#plt.xticks(d[0])
if args.logx:
    plt.xscale('log')
if args.logy:
    plt.yscale('log')
if args.xticks:
    plt.xticks(xvalues)
if args.yticks:
    plt.yticks(yvalues)
plt.show()
