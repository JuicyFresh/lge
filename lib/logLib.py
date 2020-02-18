# -*- coding: utf-8 -*-
import logging.handlers
import logging

def log(id):
	## log
	# logging.basicConfig(level=logging.INFO, format='%(levelname)s / %(asctime)s / %(funcName)s :%(lineno)d / %(message)s', \
	#                      filename='debugLevel.log', filemode='a')
	# logging.handlers.QueueHandler()
	logger = logging.getLogger(id)
	# infoHandler = logging.FileHandler('infoLevel.log')
	infoHandler = logging.handlers.RotatingFileHandler('/home/bi/work/macro/log/'+ id + '.log', 'a', maxBytes=(1024 * 1024), backupCount=3)
	printHandler = logging.StreamHandler()

	# logger.setLevel(logging.DEBUG) #최상위 logger를 최상위 레벨(DEBUG)로 해야 그 이하로 출력 가능
	logger.setLevel(logging.DEBUG)
	infoHandler.setLevel(logging.INFO)
	printHandler.setLevel(logging.INFO)

	formatter = logging.Formatter('%(levelname)s / %(asctime)s / %(funcName)s :%(lineno)d / %(message)s')
	infoHandler.setFormatter(formatter)
	printHandler.setFormatter(formatter)

	logger.addHandler(infoHandler)
	logger.addHandler(printHandler)

	return logger