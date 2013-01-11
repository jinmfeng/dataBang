import logging
import os

class EventLog:
	def __init__(self,origObj,pwdRoot):
		self.logDebug=self.getSubLogger('debug',origObj,pwdRoot)
		self.logInfo=self.getSubLogger('info',origObj,pwdRoot)
		self.logWarn=self.getSubLogger('warn',origObj,pwdRoot)
		self.logError=self.getSubLogger('error',origObj,pwdRoot)

	def debug(self,msg):
		self.logDebug.debug(msg)
	def info(self,msg):
		self.logInfo.info(msg)
	def warn(self,msg):
		self.logWarn.warn(msg)
	def error(self,msg):
		self.logError.error(msg)

	#def setLogLevel(self,level):
		#oldLevel=self.log.getEffectiveLevel()
		#self.log.setLevel(level)#info 20, debug 10
		#self.log.info("log level chanaged, from {} to {}".format(oldLevel,level))

	def getSubLogger(self,level,origObj,pwdRoot):
		if level=='debug':
			logger=logging.getLogger('debug')
		elif level=='info':
			logger=logging.getLogger('debug.info')
		elif level=='warn':
			logger=logging.getLogger('debug.info.warn')
		elif level=='error':
			logger=logging.getLogger('debug.info.warn.error')

		pwd = pwdRoot+'/spider_log/'+level
		if os.path.exists(pwd)==False:
			os.makedirs(pwd)	
		logfile=pwd+'/'+origObj+".log"

		hdlr=logging.FileHandler(logfile)
		formatter=logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
		hdlr.setFormatter(formatter)
		logger.addHandler(hdlr)

		return logger
