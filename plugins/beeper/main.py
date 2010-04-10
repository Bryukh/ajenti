import platform
from pprint import pprint, pformat

from ajenti.ui import *
from ajenti import version
from ajenti.app.helpers import CategoryPlugin, ModuleContent, EventProcessor, event
from ajenti.app.session import SessionProxy

class BeeperContent(ModuleContent):
    module = 'beeper'
    path = __file__

class Beeper(CategoryPlugin):

    text = 'Beeper'
    description = 'Beep, beep, beep!'
    icon = '/dl/beeper/icon.png'

    def on_session_start(self):
        self._text = ''
        self._form_text = []
        self._dlg_visible = False
        self._tree = TreeManager()

    def get_ui(self):
        h = UI.HContainer(
                UI.Image(file='/dl/beeper/bigicon.png'),
                UI.Spacer(width=10),
                UI.VContainer(
                    UI.Label(text='Beeper', size=5),
                    UI.Label(text='Awesome beeping action')
                )
            )
        b = UI.Button(text='Beep!')
        # TODO: maybe some autoprefixing is needed
        b['id'] = 'beeper-btn-clickme'
        a = UI.Action(text='Bang!')
        a['description'] = 'Come on, click me!'
        a['icon'] = '/dl/core/ui/icon-ok.png'
        a['id'] = 'beeper-act-clickme'
        l = UI.LinkLabel(text='Boom!')
        l['id'] = 'beeper-ll-clickme'

        f = UI.VContainer()
        for s in self._form_text:
            f.vnode(UI.Text(s))

        dlg = UI.DialogBox(
                UI.LayoutTable(
                    UI.LayoutTableRow(
                        UI.LayoutTableCell(
                            UI.TextInput(name="someInput"),
                            UI.br(),
                            UI.Select(
                                UI.SelectOption(text="option1", value="1"),
                                UI.SelectOption(text="option2", value="2"),
                                name="select"
                            ),
                            UI.br(),
                            UI.TextInputArea(name='text', width=100, height=100, text="Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Maecenas feugiat consequat diam. Maecenas metus."),
                            rowspan="3"
                        ),
                        UI.Checkbox(name='vote', text='I wanna vote for:', checked='yes'),
                    ),
                    UI.LayoutTableRow(
                        UI.Radio(name='for', text='Checkboxes', value="checkbox"),
                    ),
                    UI.LayoutTableRow(
                        UI.Radio(name='for', text='Radio buttons', checked='yes', value="radio")
                    )
                ),
                title="Test Dialog", id="testDialog", action="/handle/dialog/submit/testDialog"
            )

        b2 = UI.Button(text='Show dialog')
        b2['id'] = 'btn-dialog'

        tree =      UI.TreeContainer(
                        UI.TreeContainer(
                            UI.Label(text='789',id='123/456/789'),
                            UI.Label(text='101',id='123/456/101'),
                            text='456',id='123/456'
                        ),
                        UI.Label(text='112',id='123/112'),
                        text='123', id='123'
                    )
        self._tree.apply(tree)

        p = UI.HContainer(
                UI.VContainer(
                    h,
                    UI.Spacer(height=20),
                    UI.Label(text=self._text),
                    b,
                    l,
                    a,
                    UI.Spacer(height=50),
                    UI.DataTable(
                        UI.DataTableRow(
                            UI.Label(text='Key'),
                            UI.Label(text='Value'),
                            header=True,
                        ),
                        UI.DataTableRow(
                            UI.Label(text='12'),
                            UI.Label(text='34')
                        ),
                        UI.DataTableRow(
                            UI.Label(text='56'),
                            UI.Label(text='78')
                        )
                    )
                ),
                UI.Spacer(width=30),
                UI.VContainer(
                    f,
                    b2,
                    dlg if self._dlg_visible else None,
                    tree
                )
            )

        return p

    @event('dialog/submit')
    def on_submit(self, event, params, vars=None):
        self._form_text = []
        self._form_text.append("You submited form: %s"%str(params[0]))
        self._form_text.append("Vars:")
        for k in vars.keys():
            if len(vars.getlist(k)) > 1:
                self._form_text.append("%s = [%s]\n"%(k, ', '.join(vars.getlist(k))))
            else:
                self._form_text.append("%s = %s\n"%(k, vars.getvalue(k,'')))
        self._dlg_visible = False

    @event('button/click')
    def on_click(self, event, params, vars=None):
        if params[0] == 'beeper-btn-clickme':
            self._text += 'Beep! '
            print 'Clicked button!'
            pprint(params)
            pprint(vars)
        if params[0] == 'btn-dialog':
            self._dlg_visible = True

    @event('action/click')
    def on_aclick(self, event, params, vars=None):
        if params[0] == 'beeper-act-clickme':
            self._text += 'Bang! '
            print 'Clicked action!'
            pprint(params)
            pprint(vars)

    @event('linklabel/click')
    def on_lclick(self, event, params, vars=None):
        pprint(params)
        pprint(vars)
        if params[0] == 'beeper-ll-clickme':
            self._text += 'Boom! '
            print 'Clicked link!'
            pprint(params)
            pprint(vars)

    @event('treecontainer/click')
    def on_tclick(self, event, params, vars=None):
        self._tree.node_click('/'.join(params))
        return ''

"""
from plugin import PluginMaster, PluginInstance #Import base plugin classes from Ajenti's plugin.py
import commands
import session # Ajenti session controller
import ui # Ajenti WebUI
import log
import tools # Support for actions

# Plugins themselves consist of two parts: Master plugin and Instance plugin
# The Master plugin is launched when Ajenti server starts
# The Instance plugins are launched one per user session

class BeeperPluginMaster(PluginMaster):
	name = 'Beeper'

	def make_instance(self): # Should return a new Instance plugin
		i = BeeperPluginInstance(self)
		self.instances.append(i)
		return i


class BeeperPluginInstance(PluginInstance):
	# Standard properties
	name = 'Beeper'

	# Our custom stuff
	_tblBeeps = None
	_btnAdd = None
	_txtCmd = None
	Beeps = None

	def _on_load(self, s): # The session controller instance is passed to this method
		PluginInstance._on_load(self, s)

		# Build a category switcher for Ajenti
		c = ui.Category()
		c.text = 'Beeper'
		c.description = 'Beep-beep-beep!'
		c.icon = 'plug/beeper;icon' # This means that image is stored in plugins/beeper/icon.png
		self.category_item = c # The category_item property will be later examined by Core plugin. If it isn't None, the new Category will be added to the UI

		self.build_panel()

		# Make use of /etc/ajenti/beeper.conf
		self.Beeps = BeepingProfiles()
		log.info('BeeperPlugin', 'Started instance') # Available methods are log.info, log.warn, log.err. The first parameter is 'sender' name, the second is string being logged

	def build_panel(self):
		# The Ajenti web UI has tree-like structure based on containers

		# Make a header
		l = ui.Label('Beeper demo plugin')
		l.size = 5

		# The top block
		c = ui.HContainer([ui.Image('plug/ajentibackup;bigicon.png'), ui.Spacer(10, 1), l])

		# Profiles table
		self._tblBeeps = ui.DataTable()
		self._tblBeeps.title = 'Beeping profiles'
		self._tblBeeps.widths = [300, 100] # The column widths
		r = ui.DataTableRow([ui.Label('Params'), ui.Label('Control')])
		r.is_header = True
		self._tblBeeps.rows.append(r)

		# The main area
		d = ui.VContainer()
		d.add_element(self._tblBeeps)
		d.add_element(ui.Spacer(1,10))

		self._txtCmd = ui.Input()
		self._btnAdd = ui.Button('Add new')
		self._btnAdd.handler = self._on_add_clicked

		d.add_element(ui.Label('Beep parameters:'))
		d.add_element(self._txtCmd)
		d.add_element(self._btnAdd)


		t = ui.TreeContainer()
		tn1 = ui.TreeContainerNode('logs')
		tn2 = ui.TreeContainerNode('apache')
		tn3 = ui.Label('access.log')
		tn4 = ui.Label('error.log')
		tn5 = ui.Label('kern.log')
		t.add_element(tn1)
		tn2.add_element(tn3)
		tn2.add_element(tn4)
		tn1.add_element(tn2)
		tn1.add_element(tn5)

		s = ui.ScrollContainer([t])
		s.width = 100
		s.height = 100
		d.add_element(s)

		ta = ui.TextArea('Lorem ipsum dolor sit amet.')
		ta.width = 100
		ta.height = 100

		# Assemble the stuff altogether
		self.panel = ui.VContainer([c, d, ta])
		return


	def update(self): # The method is fired when user requests an updated UI view
		if self.panel.visible: # We can enhance Ajenti performance by not refreshing the stuff when it's not visible
			self.Beeps.parse() # Reload profiles
			self._tblBeeps.rows = [self._tblBeeps.rows[0]] # Remove all rows but the header
			for k in self.Beeps.profiles:
				l1 = ui.Link('Beep!')
				l2 = ui.Link('Delete')
				l1.handler = self._on_control_clicked
				l2.handler = self._on_control_clicked

				# We'll use custom field 'profile' to store profile this control link is for
				l1.profile = k
				l2.profile = k
				# And 'tag' property to remember what's the link for
				l1.tag = 'beep'
				l2.tag = 'delete'

				r = ui.DataTableRow([ui.Label(k), ui.HContainer([l1, l2])])
				self._tblBeeps.rows.append(r)
			return


	def _on_add_clicked(self, t, e, d): # The parameters passed are: the control that caused event, the event name and optional event data
		self.Beeps.profiles.append(self._txtCmd.text)
		self._txtCmd.text = ''
		self.Beeps.save()


	def _on_control_clicked(self, t, e, d):
		if t.tag == 'beep':
			tools.actions['beeper/beep'].run(t.profile) # Call the beeper/beep action (see below)
		if t.tag == 'delete':
			self.Beeps.profiles.remove(t.profile)
			self.Beeps.save()


# The Actions are common way for plugin interconnection. Here we define 'beep' action that can be later called by any other plugin
class BeepAction(tools.Action):
	name = 'beep'
	plugin = 'beeper'

	def run(self, d): # Argument is an optional parameter passed to the Action
		try:
			tools.actions['core/shell-run'].run('beep ' + d)
			log.warn('Beeper', 'Beeping: ' + 'beep ' + d)
		except:
			pass


# Our class to handle the /etc/ajenti/beeper.conf file
# The file contains parameter sets for beep(1) command
class BeepingProfiles:
	profiles = None

	def parse(self):
		self.profiles = []
		try:
			f = open('/etc/ajenti/beeper.conf', 'r')
			ss = f.read().splitlines()
			f.close()

			for s in ss:
				self.profiles.append(s)
		except:
			pass

	def save(self):
		f = open('/etc/ajenti/beeper.conf', 'w')
		for x in self.profiles:
			f.write(x + '\n')
		f.close()
"""