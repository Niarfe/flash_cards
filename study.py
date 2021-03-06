import csv
import os
import pryzm as pz
import random
import sys
import time
from load_dict import Dict
td = Dict('dictionary/translate_dict.csv')
red, green, dim, yellow = pz.Pryzm(echo=True).red, pz.Pryzm(echo=True).green, pz.Pryzm(echo=True)._dim, pz.Pryzm(echo=True).yellow
cyan, blue = pz.Pryzm(echo=True).cyan, pz.Pryzm(echo=True).blue

DECK=sys.argv[1]

deja_vu = []
deja_failed = []

def _input():
    try:
        response = input()
        return response.strip()
    except Exception as e:
        red(e)
        dim("let's give that another go")
        response = input()
        return response.strip()

with open(DECK, 'r') as deck:
    reader = csv.DictReader(deck)
    cards = [card for card in reader]

def show_card(txt):
    yellow(txt)

def show_right(txt):
    green(txt)

os.system('clear')
tries, wrong, state = 0, 0, 'draw'

while cards:
    cyan("State: {}".format(state))

    if state == 'draw':
        tries += 1
        card = random.choice(cards)
        os.system('clear')

        print()
        cyan("    CARDS: {}".format(len(cards)))
        cyan("    TRIES {}      DEJA {}    WRONG {}".format(tries, len(deja_vu), len(deja_failed)))
        state = 'get_answer'

    elif state == 'get_answer':
        show_card(card['WORD'])
        definition = td.lookup(card['WORD'].strip().lower())
        answer = _input()
        if answer == 'pass':
            dim('pass')
            state = 'draw'
            continue
        elif answer == 'quit' or answer == 'q':
            yellow("BYE!")
            sys.exit()

            
        if answer.strip() in card['DEF'].strip() or answer.lower() in definition.lower():
            show_right(card['DEF'])
            deja_vu.append(card)
            cards = [c for c in cards if c['WORD'] != card['WORD']]
            cyan("\n\n"+definition)
            anytext = _input()
            state = 'draw'
        else:
            # wrong answer
            red("{}".format(card['DEF']))
            deja_failed.append(card)
            cyan("\n\n"+definition)
            retry = _input()
            dim(retry)
            state = 'draw'
