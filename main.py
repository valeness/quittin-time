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
running = True

class HelloWorld(gtk.Window):

	def __init__(self):
		super(HelloWorld, self).__init__()

		self.set_title("Time Tracker")
		self.set_size_request(600, 480)
		self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))
		self.set_position(gtk.WIN_POS_CENTER)
		#self.set_border_width(20)
		
		total_hours = []
		total_minutes = []
		total_seconds = []

		prev_hours = "Hours: \n"
		prev_minutes = "Minutes: \n"
		prev_seconds = "Seconds: \n"

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
		prev_hours_label = Label(prev_hours)
		prev_hours_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFF'))
		prev_minutes_label = Label(prev_minutes)
		prev_minutes_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFF'))
		prev_seconds_label = Label(prev_seconds)
		prev_seconds_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFF'))
		total = Label("Total: \n")
		total.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFF'))

		table.attach(button, 0, 3, 1, 2)
		table.attach(text, 0, 3, 0, 1)
		table.attach(prev_hours_label, 0, 1, 2, 6)
		table.attach(prev_minutes_label, 1, 2, 2, 6)
		table.attach(prev_seconds_label, 2, 3, 2, 6)
		table.attach(total, 3, 4, 2, 6)

		vbox.pack_end(table, True, True, 0)

		self.connect("destroy", self.destroy)

		button.connect("toggled", self.timer)

		# Assign relative self variable so all methods have access
		self.text = text
		self.button = button
		self.prev_hours_label = prev_hours_label
		self.prev_minutes_label = prev_minutes_label
		self.prev_seconds_label = prev_seconds_label
		self.prev_hours = prev_hours
		self.prev_minutes = prev_minutes
		self.prev_seconds = prev_seconds
		self.total_hours = total_hours
		self.total_minutes = total_minutes
		self.total_seconds = total_seconds
		self.total = total

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
				self.prev_hours += ("%s \n") % str(int(self.hour))
				self.prev_hours_label.set_text(self.prev_hours)
				self.prev_minutes += ("%s \n") % str(int(self.minutes))
				self.prev_minutes_label.set_text(self.prev_minutes)
				self.prev_seconds += ("%0.2f \n") % self.seconds
				self.prev_seconds_label.set_text(self.prev_seconds)

				self.total_hours.append(self.hour)
				self.total_minutes.append(self.minutes)
				self.total_seconds.append(self.seconds)

				total_s = 0
				for i in self.total_seconds:
					print i
					total_s = total_s + i
				self.total.set_text(str(total_s))
				running = False
				break

	def change(self):
		show = time.time() - self.s
		hour = show / 3600
		minutes = (show % 3600) / 60
		seconds = show - (int(hour) * 3600) - (int(minutes) * 60)

		self.hour = hour
		self.minutes = minutes
		self.seconds = seconds

		display = "%s : %s : %0.2f" % (str(int(hour)), str(int(minutes)), seconds)
		self.display = display
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