DECK=decks/
#export STACK=french_vocab_-_que_vendra.csv
#export STACK=FRENCH_PORTAL-brume_livraisons.csv
export STACK=flash_cards_chateau_horreur_t1.csv
#export STACK=vocab_rlnoir_la_tache.csv
#export STACK=vocab_vendue.csv
#export STACK=remedial.csv


export CARD_STACK=${DECK}${STACK}
echo ${DECK}
echo ${STACK}
env | grep CARD_STACK
