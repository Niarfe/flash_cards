import csv
import sys

SOURCE='decks/flash_cards_chateau_horreur_t1.csv'
from load_dict import Dict

dd = Dict('dictionary/translate_dict.csv')
with open(SOURCE, 'r') as source:
    reader = csv.DictReader(source)
    for row in reader:
        print(dd.lookup(row['WORD']))
