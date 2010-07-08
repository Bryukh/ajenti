from ajenti.com import *
from ajenti import apis


class TestWebserver(Plugin):
    implements(apis.webserver.Server)
    
    name = 'Dummy'
				
	# Contorlling server state
	def getState(self):
		pass
	
	def stop(self):
		pass
	
	def start(self):
		pass
	
	def restart(self):
		pass
		
	# Configuring
	def getVirtualHosts(self):
		pass
	
	def getConfiguration(self):
		pass
	
	def getModules(self):
		pass
	
	def getVirtualHost(self, host):
		pass
	
	def addNewVirtualHost(self, hostname, args):
		pass
	
	# UI control
	def getPage(self, pageName ):
		pass