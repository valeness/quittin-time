import pygtk
pygtk.require('2.0')
import gtk
from gtk import Button, Layout, Label, Table

import time
import threading
import gobject
gtk.gdk.threads_init()

hellon = 0
counter = 0

class HelloWorld(gtk.Window):

	def __init__(self):
		super(HelloWorld, self).__init__()

		self.set_title("Time Tracker")
		self.set_size_request(600, 480)
		self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))
		self.set_position(gtk.WIN_POS_CENTER)
		#self.set_border_width(20)

		vbox = gtk.VBox(False, 2)

		mb = gtk.MenuBar()
		filemenu = gtk.Menu()
		filem = gtk.MenuItem("File")
		filem.set_submenu(filemenu)
		mb.append(filem)

		vbox.pack_start(mb, False, False, 0)

		table = gtk.Table(5, 2, True)

		button = gtk.ToggleButton(label = "Start")
		button2 = Button("Test")

		text = Label("Hello World")
		text.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFF'))

		table.attach(button, 0, 4, 1, 2)
		#table.attach(button2, 0, 4, 2, 3)
		table.attach(text, 0, 4, 0, 1)

		vbox.pack_end(table, True, True, 0)

		self.connect("destroy", gtk.main_quit)

		button.connect("toggled", self.timer)

		self.text = text
		self.button = button

		self.add(vbox)
		self.show_all()

	def hello(self, widget, data=None):
		global hellon
		self.text.set_label(str(hellon))
		hellon += 1

	def timer(self, widget):
		if widget.get_active():
			self.s = time.time()
			threading.Thread(target = self.update).start()
			widget.set_label("Stop")
		else:
			widget.set_label("Start")

	def update(self):
		i = 0
		while 1:
			time.sleep(0.01)
			gobject.idle_add(self.change)
			#print i
			i = i + 1
			if self.button.get_active() == 0:
				break

	def change(self):
		show = time.time() - self.s
		hour = show / 3600
		minutes = (show % 3600) / 60
		seconds = show - (int(hour) * 3600) - (int(minutes) * 60)
		display = "%s : %s : %0.2f" % (str(int(hour)), str(int(minutes)), seconds)
		self.text.set_text(display)

	def destroy(self, widget, data=None):
		gtk.main_quit()

	def main(self):
		gtk.main()

if __name__ == "__main__":
	hello = HelloWorld()
	hello.main()