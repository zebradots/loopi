#!/bin/python3
#
# loopi: Seamless looped video playback
# Copyright (C) 2022 Zebradots Software
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import os
import signal
import hashlib
import re
import random, string
import shlex
import subprocess
from subprocess import Popen
import sys
import time
import tkinter as tk
from tkinter import *

print()
print("------------------------------------------------------------------------")
print("loopi: Simple looped video playback")
print("http://github.com/")
print("------------------------------------------------------------------------")
print()
print("Python version: " + sys.version)
print()

www_dir = "/var/www/"								# Web server HTML location
media_dir = www_dir + "filegator/repository/"		# Media file storage
countdown = 10										# Countdown before playback
interface = "wlan0"									# Device to create host access point

class loopi_app():

	def __init__(self):
		global start_time
		self.read_wifi_conf()
		bg_color = "#800080"
		fg_color = "#b933b9"
		start_time = 30
		# Root setup
		self.root = tk.Tk()
		self.root.wm_overrideredirect(True)
		self.root.configure(bg=bg_color)
		self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
		self.root.bind("<Button-1>", lambda evt: self.root.destroy())
		# Logo
		try:
			img = PhotoImage(file=www_dir+'html/assets/loopi.png')
			self.logo = Label(self.root, image=img, borderwidth=0, highlightthickness=0)
			self.logo.pack(pady=(220, 140))
		except:
			pass
		# File detection text
		self.label_files = tk.Label(text="", font=("Roboto", 24), fg=fg_color, bg=bg_color)
		self.label_files.pack(pady=20)
		# Playback status
		self.label_status = tk.Label(text="", font=("Roboto", 60, "bold"), fg="white", bg=bg_color)
		self.label_status.pack(pady=40)
		# WiFi access text
		self.text_net = tk.Text(self.root, height=2, font="Roboto 24", bg=bg_color, fg=fg_color)
		self.text_net.tag_configure("center", justify="center")
		self.text_net.tag_configure("normal", font="Roboto 24 normal", foreground=fg_color)
		self.text_net.tag_configure("bold", font="Roboto 24 bold", foreground="white")
		self.text_net.insert("1.0", "Connect to WiFi network ")
		self.text_net.tag_add("center", "1.0", "end")
		self.text_net.insert("end", ssid, "bold")
		self.text_net.insert("end", " with password ", "normal")
		self.text_net.insert("end", pw, "bold")
		self.text_net.insert("2.0", "\nand open ")
		self.text_net.insert("end", "http://loopi", "bold")
		self.text_net.insert("end", " to manage media files", "normal")
		self.text_net.tag_add("center", "2.0", "end")
		self.text_net.configure(state="disabled", highlightthickness=0, borderwidth=0)
		self.text_net.pack(pady=20)
		# Begin execution
		self.check_media()
		self.root.mainloop()

	def check_media(self):
		# Check for media files
		global start_time, media
		self.label_files.configure(text="Looking for media files...")
		media = []
		self.find_files()
		print("Found "+str(len(media))+f" media files in {media_dir}:")
		for m in media:
			print("  * ", os.path.basename(m))
		if len(media)==0:
			self.root.state('normal')
			self.label_files.configure(text="No media files found.")
			self.label_status.configure(text="Waiting for media")
			start_time = 0
			self.root.after(1000, self.check_media)
			return
		elif len(media)==1:
			self.label_files.configure(text="Media file found. Ready to begin playback.")
		elif len(media)>1:
			self.label_files.configure(text="Found "+str(len(media))+" media files. Only first file is played.")
		start_time = time.time() + countdown
		self.update_status()
		print("Scheduled to start at: "+str(start_time))

	def find_files(self):
		# Get list of media files in the storage location
		global media, file_hash
		file_info = ""
		files = os.listdir(media_dir)
		for f in files:
			if f.endswith(".avi") or f.endswith(".mov") or f.endswith(".mpg") or f.endswith(".mp4"):		
				media.append(media_dir + f.replace(' ', '\ '))
				file_info += f + ": " + str(os.stat(media_dir + f).st_mtime) + "\n"
		media.sort()
		file_hash = hashlib.md5(file_info.encode('utf-8')).hexdigest()

	def update_status(self):
		# Update the status text
		global player_pid
		if start_time==0:
			return
		cd = round(start_time - time.time())
		if cd >= 1:
			self.label_status.configure(text="Playback starts in " + str(cd) + " seconds")
			self.root.after(100, self.update_status)
		else:
			self.label_status.configure(text="Playback started")
			self.root.state('withdrawn')
			print("Starting playback at " + time.strftime('%Y-%m-%d %H:%M:%S'))
			# Begin playback
			player_pid = 0
			self.monitor_playback()
			
	def monitor_playback(self):
		# Start or confirm playback running
		global p, player_pid, start_time, media
		refresh = 1000
		if player_pid == 0:
			# Execute new playback process that permits keyboard controls
			cmd = "xterm -fullscreen -fg black -bg black -e omxplayer -r --loop"
			cmd += " " + media[0]
			print("Executing: " + cmd)
			p = Popen(shlex.split(cmd))	# Supports filenames with spaces
			player_pid = p.pid
			print("Created new playback process PID:", p.pid)
			exit
			self.root.after(refresh, self.monitor_playback)
		else:
			# Check status of existing process
			ps = p.poll()
			# The poll() method returns 'None' if process is running,
			# else it returns the exit code
			if str(ps) != "None":
				print("Playback process exited with code:", ps)
				player_pid = 0
				start_time = 0
				self.root.state('normal')
				self.check_media()
			else:
				# Playback in progress
				old_hash = file_hash
				self.find_files()
				if not old_hash == file_hash:
					print("Files have changed. Updating media list.")
					os.kill(player_pid, signal.SIGTERM)
					self.root.state('normal')
					self.check_media()
				else:
					self.root.after(refresh, self.monitor_playback)

	def read_wifi_conf(self):
		# Read host AP configuration
		global ssid, pw
		conf = "/etc/hostapd/hostapd.conf"
		try:
			with open(conf, "r") as f:
				content = f.read()
			matches = re.search('(?s)ssid=(.*?)\n', content)
			ssid = matches.group(1)
			matches = re.search('(?s)wpa_passphrase=(.*?)\n', content)
			pw = matches.group(1)
		except:
			print("WARNING: Failed to load wifi config from hostapd.conf. Continuing anyway.")				
			ssid = "UNKNOWN"
			pw = "UNKNOWN"
		print("WiFi SSID: "+ssid)
		print("WiFi pass: "+pw)

# Get started
loopi = loopi_app()
