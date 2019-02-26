####################################################################################################
# Author: Edgar Oregel
# Date: 6/20/18
# File: interface.py
# Description: Controls the UI of the application and its components
####################################################################################################


#########
#Imports#
#########
import os
import re
import logging
from tkinter import *
from tkinter import messagebox
import pptxCreation as PPTX

##################
#Global Variables#
##################
ALL_PPTX_SLIDES = []
#Holds all of the main widgets for the entire interface (pptx_name, path)
ALL_WIDGETS = {}
#Just holds label fields to add/remove dynamically
SONG_LABELS = []
#Holds all the input fields for the song names
SONG_ENTRIES = []

############
#Main Class#
############
class ConcatPPTXInterface():
	def __init__(self, masterWindow):
		#Master Window Settings
		self.master = masterWindow
		self.master.title("Create PowerPoint")		
		#Class variables
		self.entry_width = 30
		self.button_width = 11
		self.padx = 10
		self.pady = 10
		self.row = self.col = 0
		#Track for checking limit
		self.song_count = 1
		self.song_limit = 7

		#Instantiate logger
		self.logger = logging.getLogger()
		handler = logging.StreamHandler()
		formatter = logging.Formatter(
		'%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)
		self.logger.setLevel(logging.DEBUG)

		#Create items on top frame
		self.createTopFrameWidgets()
		#Create bottom widgets (add songs)
		self.createAddSongsWidgets()


	#Creates top items (titleLabel, pptx name, where_to_look)
	def createTopFrameWidgets(self):
		#Set top frame
		self.topFrame = Frame(self.master)
		self.topFrame.pack(padx=self.padx, pady=self.pady)
		#Set title
		titleLabel = Label(self.topFrame, text="Create PowerPoint", font=("", 18))
		titleLabel.pack()

		#New frame for top entry fields (name/where_to_look)
		self.widgetFrame = Frame(self.master)
		self.widgetFrame.pack(padx=self.padx, pady=self.pady)
		#Set pptx name
		pptx_name_label = Label(self.widgetFrame, text="PowerPoint Name: ")
		pptx_name_label.grid(row=self.row,column=self.col)
		pptx_name_entry = Entry(self.widgetFrame, width = self.entry_width)
		ALL_WIDGETS["pptx_name"] = pptx_name_entry
		self.col += 1
		pptx_name_entry.grid(row=self.row,column=self.col)

		self.row += 1
		self.col = 0
		#Set where_to_look
		path_label = Label(self.widgetFrame, text="Path: ")
		path_label.grid(row=self.row,column=self.col, sticky=E)
		path_entry = Entry(self.widgetFrame, width=self.entry_width)
		ALL_WIDGETS["path"] = path_entry
		self.col += 1
		path_entry.grid(row=self.row,column=self.col)

	#Creates the add songs widgets for users to add songs to search for
	def createAddSongsWidgets(self):
		#Default Add 1 entry field
		self.songFrame = Frame(self.master)
		self.songFrame.pack()

		self.row += 1
		self.col = 1

		add_song_label = Label(self.widgetFrame, text="Add Song: ", font=("",14))
		add_song_label.grid(row=self.row, column=self.col, sticky=W)

		self.row += 1
		self.col = 0
		#By default start with one song
		song_name_label = Label(self.widgetFrame, text="Song #/Name: ")
		song_name_label.grid(row=self.row, column=self.col, sticky=E)
		self.col += 1
		song_name_entry = Entry(self.widgetFrame, width=self.entry_width)
		song_name_entry.grid(row=self.row, column=self.col)

		#Addd widgets for validation and remove on Remove Button
		ALL_WIDGETS["song"] = [song_name_entry]
		SONG_LABELS.append(song_name_label)
		SONG_ENTRIES.append(song_name_entry)

		self.row += 1
		self.col = 1
		#Add more songs button
		self.add_song_button = Button(self.widgetFrame, text="Add Song", width=self.button_width, command = self.addAnotherSong)
		self.add_song_button.grid(row=self.row, column=self.col, sticky=W, pady=(self.pady,0))

		
		#Remove Song button
		self.remove_song_button = Button(self.widgetFrame, text="Remove Song", command = self.removeSongEntry)
		self.remove_song_button.grid(row=self.row, column=self.col, sticky=E, pady=(self.pady,0))

		self.row += 1
		#Create powerpoint button
		self.create_pptx_button = Button(self.widgetFrame, text="Create PowerPoint", command = self.createPowerPoint)
		self.create_pptx_button.grid(row=self.row, column=self.col, sticky=S+E, pady=(self.pady,0))


###################
#Utility Functions#
###################
	
	#Handles the actions required to create powerpoint
	def createPowerPoint(self):
		pp = PPTX.PPTX()
		
		#validate all input
		self.validateInput()



	#Adds another label and entry widget to add another song 
	def addAnotherSong(self):
		#Check if reached song limit
		if self.songLimitReached():
			self.logger.error("Error")
			messagebox.showerror("Song Limit", "You've reached the song limit of {} songs.".format(self.song_limit))
			return
		
		#Increment song count
		self.song_count += 1

		#Remove add another song button first to add label/entry
		self.add_song_button.destroy()
		self.remove_song_button.destroy()
		self.create_pptx_button.destroy()

		self.col = 0
		#By default start with one song
		song_name_label = Label(self.widgetFrame, text="Song Name: ")
		song_name_label.grid(row=self.row, column=self.col, sticky=E)
		self.col += 1
		song_name_entry = Entry(self.widgetFrame, width=self.entry_width)
		song_name_entry.grid(row=self.row, column=self.col)

		#Add widgets for validation and removal on Remove Button
		ALL_WIDGETS["song"].append(song_name_entry)
		SONG_LABELS.append(song_name_label)
		SONG_ENTRIES.append(song_name_entry)

		self.row += 1
		self.col = 1
		#Add more songs button
		self.add_song_button = Button(self.widgetFrame, text="Add Song", width=self.button_width, command = self.addAnotherSong)
		self.add_song_button.grid(row=self.row, column=self.col, sticky=W, pady=(self.pady,0))
		
		#Remove Song button
		self.remove_song_button = Button(self.widgetFrame, text="Remove Song", command = self.removeSongEntry)
		self.remove_song_button.grid(row=self.row, column=self.col, sticky=E, pady=(self.pady,0))

		self.row += 1
		#Create powerpoint button
		self.create_pptx_button = Button(self.widgetFrame, text="Create PowerPoint", command = self.createPowerPoint)
		self.create_pptx_button.grid(row=self.row, column=self.col, sticky=S+E, pady=(self.pady,0))

		
	#Removes a song entry widgets
	def removeSongEntry(self):
		#Check that there's more than one song label/entry left
		if len(SONG_LABELS) > 1:
			self.logger.info("Removing song label and entry widget...")
			#Destroy the widgets
			SONG_LABELS[-1].destroy()
			SONG_ENTRIES[-1].destroy()

			#Remove them from the list
			del SONG_LABELS[-1]
			del SONG_ENTRIES[-1]
			self.logger.info("Removed.")
			self.song_count -= 1
		else:
			self.logger.error("There's only one song widget left trying to be removed")
			messagebox.showerror("Last Song", "You can't remove the last song entry field and label.")
			return

	#Checks if reached song limit
	def songLimitReached(self):
		if self.song_count > self.song_limit:
			return True
		return False


#################
#Data Validation#
#################

	#Parent validation function
	def validateInput(self):
		if not self.validatePath():
			messagebox.showerror("Bath Path", "That path does not exist. Please double check the path you gave.")
			return False


	#Validates directory path
	def validatePath(self):
		path = ALL_WIDGETS["path"].get()
		print(path)
		#check if path
		if not path:
			self.logger.info("Empty Path: " + path)
			messagebox.showerror("No Path", "Please provide a path to look for files.")
			return False
		try:
			if not os.path.isdir(path):
				return False
			return True
		except Exception as ex:
			self.logger.error("[validatePath]: " + ex)
			messagebox.showerror("Bad Path", "Something went wrong looking for the path you provided: \n\nErr:{}".format(ex))

		


#Window definition and start of mainloop which actually executes the gui
root = Tk()
my_app = ConcatPPTXInterface(root)
root.mainloop()