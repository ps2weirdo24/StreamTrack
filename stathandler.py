
"""

How to use this script:

Call this script from the command line, there are 3 arguments that can be used

1. Channel to collect data from i.e "clgdoublelift" or "imaqtpie" (Not an optional argument)

2. Amount of time (in seconds) that the recording will be i.e "600" or "1200" (Optional argument, defaults to 600 seconds)

3. Quality of the video captured, options include "low", "high", "medium" or "best"

A full example:

python stathandler.py imaqtpie 1200 high
 

"""

import os
from os import path
from datetime import datetime, timedelta
import time
import unirest
import sys
from chatbot import ChatCollector

def is_online(channel):
	url = "https://api.twitch.tv/kraken/streams/%s" % channel
	response = unirest.get(url)
	if response.body["stream"] == None:
		return False
	else:
		return True

class MainCollect:

	def __init__(self, channel, dump_often=600, quality="high"):
		"""
			The channel var should be a string formated as "voyboy" or "aphromoo"
			the dump_often var should be a int specifying the amount of seconds in each data dump
			the continue_dumps var should be a bool specifying to continue gathering data after the first data dump
			the quality var should be a string specifying what quality the stream should be recorded in
		"""

		start_time = datetime.now()
		end_time = start_time + timedelta(seconds=dump_often)
		self.start_time_format = datetime.strftime(start_time,"%H%M")
		end_time_format = datetime.strftime(end_time,"%H%M")
		duration_format = "%s-%s" % (self.start_time_format,end_time_format)
		self.format_date = datetime.strftime(start_time,"%m-%d-%Y")

		working_dir = "Data/%s/%s/%s" % (channel,self.format_date,duration_format)

		self.working_dir = working_dir
		self.duration = duration_format
		self.start_time = start_time
		self.end_time = end_time
		self.channel = channel
		self.dump_often = dump_often
		self.quality = quality
		self.log_file = "%s_log.txt" % (channel)
		self.abs_log_file = "Data/%s/%s" % (channel,self.log_file)

		if path.exists("Data/%s" % channel):
			pass
		else:
			os.mkdir("Data/%s" % channel)
		if path.exists(self.abs_log_file):
			pass
		else:
			log_file_cons = open(self.abs_log_file, "w")
			log_file_cons.write("%s log file\n========\n" % (channel))
			log_file_cons.close()
		if path.exists("Data/%s/%s" % (channel,self.format_date)):
			pass
		else:
			os.mkdir("Data/%s/%s" % (channel,self.format_date))
		if path.exists(working_dir):
			pass
		else:
			os.mkdir(working_dir)

		"""
		Code below gathers strean data from the Twitch.tv API
		"""

		# self.api_url = "https://api.twitch.tv/kraken/streams/%s" % self.channel
		# self.api_response = unirest.get(self.api_url)

		# self.viewer_count = self.api_response.body["stream"]["viewers"]
		# self.stream_delay = self.api_response.body["stream"]["channel"]["delay"]

	def chat_bot_constructor(self):
		output_filename = "%s/%s_%s.txt" % (self.working_dir,self.channel,self.duration)
		return ChatCollector(self.channel,output_filename,self.dump_often)

	def is_online(self):
		url = "https://api.twitch.tv/kraken/streams/%s" % self.channel
		response = unirest.get(url)
		if response.body["stream"] == None:
			return False
		else:
			self.viewer_count = response.body["stream"]["viewers"]
			self.game_being_played = response.body["stream"]["game"]
			self.stream_delay = response.body["stream"]["channel"]["delay"]
			return True

	def write_to_log(self,message):
		preface = "<%s  %s>  " % (self.format_date,self.start_time_format)
		log_writer = open(self.abs_log_file,"a")
		log_writer.write("%s%s\n" % (preface,message))
		log_writer.close()


	def run(self):
		my_cwd = (os.getcwd().replace("\\","/") + "/")
		new_dir = my_cwd + self.working_dir
		if self.is_online:
			robot_message = "online,%s" % (new_dir)
		else:
			robot_message = "offline,%s" % (new_dir)
		robot_talk = open("robot_talk.txt","w")
		robot_talk.write(robot_message)
		robot_talk.close()
		self.chat_bot = self.chat_bot_constructor()
		self.chat_bot.start()

		
argList = sys.argv

if len(argList) == 1:
	print "DEBUG MODE"
	cli = MainCollect("voyboy", dump_often=90)
elif len(argList) == 2:
	cli = MainCollect(argList[1])
elif len(argList) == 3:
	cli = MainCollect(argList[1],dump_often=int(argList[2]))
elif len(argList) == 4:
	cli = MainCollect(argList[1],dump_often=int(argList[2]),quality=argList[3])
else:
	print "ERROR: Invalid arguments entered"

if not cli.is_online():
	warn_offline = "The channel entered is offline"
	print warn_offline
	cli.write_to_log(warn_offline)
	cli.run()
else:
	online_message = "Chat bot initialized.\n    Viewer Count: %s \n    Time Delay: %s \n    Game: %s " % (str(cli.viewer_count), str(cli.stream_delay), str(cli.game_being_played))
	cli.write_to_log(online_message)
	cli.run()

