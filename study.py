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
    reader = csv.reader(deck, delimiter=',')
    cards = [card for card in reader]

def show_card(txt):
    yellow(txt)

def show_right(txt):
    green(txt)

os.system('clear')
right, wrong, state = 0, 0, 'draw'

while cards:
    cyan("State: {}".format(state))

    if state == 'draw':
        pick = random.randint(0, len(cards)-1)
        card = cards[pick]
        os.system('clear')

        print()
        cyan("    CARDS: {}".format(len(cards)))
        cyan("    RIGHT {}      WRONG {}".format(right, wrong))
        state = 'get_answer'

    elif state == 'get_answer':
        show_card(card[0])
        definition = td.lookup(card[0].strip().lower())
        answer = _input()
        if answer == 'pass':
            dim('pass')
            del cards[pick]
            state = 'draw'
        elif answer == 'quit':
            yellow("BYE!")
            sys.exit()
        elif answer.strip() == card[1].strip():
            # right answer
            blue("answer.strip() == card[1].strip()")
            right += 1
            show_right(card[1])
            del cards[pick]
            cyan("\n\n"+definition)
            blue("Sleeping 5 seconds")
            time.sleep(5)
            state = 'draw'
        else:
            # wrong answer
            wrong += 1
            red("{}".format(card[1]))
            cyan("\n\n"+definition)
            retry = _input()
            dim(retry)
            state = 'draw'
