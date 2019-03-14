#!/usr/bin/env python3
# Parse args
from praktipy import TableHandler
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("TableFile", help='Path to the table file. E.g. "Table.txt"')
parser.add_argument("-m", "--meanValues", dest="mean", help="Print mean values", action="store_true")
parser.add_argument("-t", "--tex", dest="tex", help="Write a Tex Table to file", metavar="TEXFILE")
args = parser.parse_args()

th = TableHandler(args.TableFile)

print("Found following table:")
for i in th.table:
    print(i)
print("==============")

if args.mean:
    print("Mean values:")
    for i in th.getMeanValues().items():
        print(str(i[0])+":", i[1])
    print("==============")

if args.tex:
    th.makeTexTable(args.tex)
    print("Generated tex table as", args.tex)
