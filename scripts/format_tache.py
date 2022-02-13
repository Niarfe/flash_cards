"""
Reformat file, so that every two lines becomes left and right cols in a csv.

line1
line2
line3
line4

becomes

line1,line2
line3,line4
"""
import sys


SOURCE = sys.argv[1]
assert SOURCE, "pass in the target file"

import csv
csv_columns = ['WORD','DEF']
dict_data = []
word = None
defi = None
with open(SOURCE, 'r') as source:
    for idx, line in enumerate(source):
        if (idx % 2) != 0:
            defi = line.strip().lower()
            dict_data.append({ 'WORD': word, 'DEF': defi } )
            word = None
            defi = None
        else:
            word = line.strip().strip('.').lower()

csv_file = "reformatted.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
except IOError:
    print("I/O error")
