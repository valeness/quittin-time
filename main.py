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
old_s = []
running = True

class HelloWorld(gtk.Window):

	def __init__(self):
		super(HelloWorld, self).__init__()

		self.set_title("Time Tracker")
		self.set_size_request(600, 480)
		self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))
		self.set_position(gtk.WIN_POS_CENTER)
		#self.set_border_width(20)
		
		prev_text = "Previous Times: \n"

		vbox = gtk.VBox(False, 2)

		mb = gtk.MenuBar()
		filemenu = gtk.Menu()
		filem = gtk.MenuItem("File")
		filem.set_submenu(filemenu)
		exit = gtk.MenuItem("Exit")
		exit.connect("activate", gtk.main_quit)
		filemenu.append(exit)
		mb.append(filem)

		vbox.pack_start(mb, False, False, 0)

		table = gtk.Table(5, 6, True)

		button = gtk.ToggleButton(label = "Start")
		button2 = Button("Test")

		text = Label("Hello World")
		text.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFF'))
		previous = Label(prev_text)
		previous.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFF'))

		table.attach(button, 0, 3, 1, 2)
		table.attach(text, 0, 3, 0, 1)
		table.attach(previous, 0, 1, 2, 6)

		vbox.pack_end(table, True, True, 0)

		self.connect("destroy", self.destroy)

		button.connect("toggled", self.timer)

		self.text = text
		self.button = button
		self.previous = previous
		self.prev_text = prev_text

		self.add(vbox)
		self.show_all()

	def hello(self, widget, data=None):
		global hellon
		self.text.set_label(str(hellon))
		hellon += 1

	def timer(self, widget):
		if widget.get_active():
			self.s = time.time()
			global running
			running = True
			threading.Thread(target = self.update).start()
			widget.set_label("Stop")
		else:
			widget.set_label("Start")

	def update(self):
		global running
		i = 0
		while running:
			time.sleep(0.01)
			gobject.idle_add(self.change)
			#print i
			i = i + 1
			if self.button.get_active() == 0:
				global display
				self.prev_text += ("%s \n") % display
				self.previous.set_text(self.prev_text)
				running = False
				break

	def change(self):
		show = time.time() - self.s
		hour = show / 3600
		minutes = (show % 3600) / 60
		seconds = show - (int(hour) * 3600) - (int(minutes) * 60)
		global display
		display = "%s : %s : %0.2f" % (str(int(hour)), str(int(minutes)), seconds)
		self.text.set_text(display)

	def destroy(self, widget, data=None):
		global running
		running = False
		gtk.main_quit()

	def main(self):
		gtk.main()

if __name__ == "__main__":
	hello = HelloWorld()
	hello.main()