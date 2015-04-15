import pygtk
pygtk.require('2.0')
import gtk
from gtk import Button, Layout, Label, Table

import time
import threading
import gobject
gtk.gdk.threads_init()

running = True

class HelloWorld(gtk.Window):

	def __init__(self):
		super(HelloWorld, self).__init__()

		self.set_title("Time Tracker")
		self.set_size_request(600, 480)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_decorated(setting=False)
		#self.set_border_width(20)

		scrolled_window = gtk.ScrolledWindow(hadjustment=None, vadjustment=None)

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

		table = gtk.Table(6, 6, True)
		table2 = gtk.Table(3, 1, False)

		button = gtk.ToggleButton(label = "Start")
		button2 = Button("Test")

		text = Label("Hello World")
		prev_hours_label = Label(prev_hours)
		prev_minutes_label = Label(prev_minutes)
		prev_seconds_label = Label(prev_seconds)
		
		prev_hours_label.set_alignment(xalign=0.5, yalign=0)
		prev_minutes_label.set_alignment(xalign=0.5, yalign=0)
		prev_seconds_label.set_alignment(xalign=0.5, yalign=0)

		total_seconds_label = Label("Total Seconds \n 0")
		total_minutes_label = Label("Total Minutes \n 0")
		total_hours_label = Label("Total Hours \n 0")

		table.attach(button, 0, 3, 1, 2)
		table.attach(text, 0, 3, 0, 1)
		
		#table.attach(prev_hours_label, 0, 1, 2, 3)
		#table.attach(prev_minutes_label, 1, 2, 2, 3)
		#table.attach(prev_seconds_label, 2, 3, 2, 3)
		
		table2.attach(prev_hours_label, 0, 1, 0, 1)
		table2.attach(prev_minutes_label, 1, 2, 0, 1)
		table2.attach(prev_seconds_label, 2, 3, 0, 1)
		scrolled_window.add_with_viewport(table2)

		table.attach(scrolled_window, 0, 3, 2, 6)

		table.attach(total_seconds_label, 5, 6, 2, 3)
		table.attach(total_minutes_label, 4, 5, 2, 3)
		table.attach(total_hours_label, 3, 4, 2, 3)

		vbox.pack_start(table, True, True, 0)


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
		self.total_seconds_label = total_seconds_label
		self.total_minutes_label = total_minutes_label
		self.total_hours_label = total_hours_label

		self.add(vbox)
		self.show_all()

	def hello(self, widget, data=None):
		global hellon
		self.text.set_label(str(hellon))
		hellon += 1

	def timer(self, widget):
		if widget.get_active():
			self.s = time.time()
			#print self.s
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
				total_m = 0
				total_h = 0

				for i in self.total_seconds:
					# Find how many minutes in total seconds and append it to total_minutes
					self.total_minutes.append(int(total_s / 60))

					# Get total seconds in this 'round'
					total_s = total_s + i
					# Find remainder and display that as the total "seconds"
					total_s = total_s % 60
				for i in self.total_minutes:
					total_m = total_m + i
				for i in self.total_hours:
					total_h = total_h + i

				self.total_seconds_label.set_text("Total Seconds \n %0.2f" % total_s)
				self.total_minutes_label.set_text("Total Minutes \n %0i" % total_m)
				self.total_hours_label.set_text("Total Hours \n %0i" % total_h)
				running = False
				break

	def change(self):
		show = time.time() - self.s
		hour = show / 3600
		minutes = (show % 3600) / 60
		seconds = show - (int(hour) * 3600) - (int(minutes) * 60)
		tseconds = show
		#print tseconds

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