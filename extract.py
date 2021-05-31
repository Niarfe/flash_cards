# Simple reformatter to get lyrics into googlesheets
# * find lyrics in google
# * select to translate so you get two lines per...
# * cut and paste the text into a <song>.txt file
# * run this script with that file as argument
# * open sheet in google and import, select TAB as separator
import sys

SOURCE=sys.argv[1]

def _is_empty(line):
    return len(line.strip()) == 0

with open(SOURCE, 'r') as source:
    lines = [line.strip() for line in source if len(line.strip()) > 0]

pair = []
with open(SOURCE.replace('.txt', '.tsv'), 'w') as target:
    for idx in range(int(len(lines)/2)):
        target.write("\t".join(lines[idx*2:idx*2+2])+"\n")
