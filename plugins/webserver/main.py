from ajenti.ui import *
from ajenti.com import implements
from ajenti.app.api import ICategoryProvider
from ajenti.app.helpers import *
from ajenti import apis

class WebServerPlugin(CategoryPlugin):
    implements((ICategoryProvider, 110))

    text = 'Web Server'
    icon = '/dl/webserver/icon.png'

    backends = None
    backend = None
    
    def on_init(self):
        self._logging_in = not self.config.has_option('webserver', 'backend')
        self.backends = [b.name for b in self.app.grab_plugins(apis.webserver.Server)] 
        if self.config.has_option('webserver', 'backend'):
            self.backend = self.app.grab_plugins(apis.sql.IDBBackend, 
                            lambda x: x.name == self.config.get('webserver', 'backend'))[0]
            
    def on_session_start(self):
        self._labeltext = ''
        self._logging_in = False
        self._tab = 0

    def get_ui(self):
        self.on_init()
        
        status = UI.VContainer()
        
        for b in self.backends:
            but = UI.Action(text=b)
            but['id'] = 'server-%s' % b
            status.append(but)
        
        panel = UI.PluginPanel(status, title='Web Server', icon='/dl/webserver/icon.png')
        
        panel.appendChild(self.get_default_ui())

        return panel

    def get_default_ui(self):
        t = UI.TabControl(active=self._tab)
        return t


class WebServerContent(ModuleContent):
    module = 'webserver'
    path = __file__
