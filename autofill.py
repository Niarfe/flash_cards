import csv
import sys

SOURCE='decks/flash_cards_chateau_horreur_t1.csv'
#SOURCE='decks/vendue.csv'
from load_dict import Dict

dd = Dict('dictionary/translate_dict.csv')
with open(SOURCE, 'r') as source:
    reader = csv.DictReader(source)
    for row in reader:
        defi = dd.lookup(row['WORD'])
        if defi.startswith("No def"):
            print(row)
        elif defi == None:
            print(row, "None")
        else:
            #print(defi)
            pass
