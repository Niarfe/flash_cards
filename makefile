default:
	@cat makefile

study:
	. setdeck.sh && python study.py $${CARD_STACK}


random:
	. setdeck.sh && cat $${CARD_STACK} | sort -R | head -n 5 > random.csv
	python study.py random.csv

test:
	pytest -vvx load_dict.py

run:
	python study.py decks/flash_cards_chateau_horreur_t1.csv 

repl:
	ipython -i load_dict.py
