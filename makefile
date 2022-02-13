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
	#python study.py decks/flash_cards_chateau_horreur_t1.csv 
	python study.py decks/vendue.csv 

repl:
	ipython -i load_dict.py

update:
	. setdeck.sh && \
	  mv /Volumes/Transcend/Downloads/PORTAL_FRENCH\ -\ ${STACK} ${CARD_STACK}

load:
	python bin/load.py
