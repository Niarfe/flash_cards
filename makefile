default:
	@cat makefile

study:
	. setdeck.sh && python study.py $${CARD_STACK}
