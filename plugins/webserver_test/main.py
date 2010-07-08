from ajenti.com import *
from ajenti import apis


class TestWebserver(Plugin):
    implements(apis.webserver.Server)
    
    name = 'Dummy'
				
	# Contorlling server state
	def getState(self):
		return 1
	
	def stop(self):
		return 1
	
	def start(self):
		return 1
	
	def restart(self):
		return 1
		
	# Configuring
	def getVirtualHosts(self):
		return 1
	
	def getConfiguration(self):
		return 1
	
	def getModules(self):
		return 1
	
	def getVirtualHost(self, host):
		return 1
	
	def addNewVirtualHost(self, hostname, args):
		return 1
	
	# UI control
	def getPage(self, pageName ):
		return 1