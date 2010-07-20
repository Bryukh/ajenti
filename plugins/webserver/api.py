from ajenti.com import *
from ajenti.apis import API

class WebServer(API):
	class Server(Interface):
		name = 'Unknown'
		
		
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