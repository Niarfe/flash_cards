import csv
import os
import pryzm as pz
import random
import sys
import time
red, green, dim, yellow = pz.Pryzm(echo=True).red, pz.Pryzm(echo=True).green, pz.Pryzm(echo=True)._dim, pz.Pryzm(echo=True).yellow
cyan, blue = pz.Pryzm(echo=False).cyan, pz.Pryzm(echo=True).blue

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

skip_words = ['continuar', 'Vendrá', 'vendrá', 'pensar', 'pierdo', 'acabará', 'camino']

os.system('clear')
right = 0
wrong = 0
state = 'draw'

while cards:

    if state == 'draw':
        cyan("State: draw")
        pick = random.randint(0, len(cards)-1)
        card = cards[pick]
        os.system('clear')
        blue("CARDS: {}".format(len(cards)))
        blue("RIGHT {}      WRONG {}".format(right, wrong))
        state = 'sort'

    elif state == 'sort':
        cyan("State: sort")
        if next((match for match in skip_words if match in card[1]), None):
            del cards[pick]
            state = 'draw'
        else:
            state = 'get_answer'

    elif state == 'get_answer':
        cyan("State: get_answer")
        yellow(card[0])
        answer = _input()
        if answer == 'pass':
            dim('pass')
            del cards[pick]
            state = 'draw'
        elif answer == 'quit':
            yellow("BYE!")
            sys.exit()
        elif answer.strip() == card[1].strip():
            cyan("answer.strip() == card[1].strip()")
            right += 1
            green(card[1])
            del cards[pick]
            time.sleep(5)
            state = 'draw'
        else:
            wrong += 1
            red("{}".format(card[1]))
            retry = _input()
            dim(retry)
            state = 'draw'
