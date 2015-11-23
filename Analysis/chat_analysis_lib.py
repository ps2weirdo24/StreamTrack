#!/usr/bin/env python

from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np

class ChatAnalysis():
	def __init__(self):
		self.filename = None

	def load_file(self, filename):
		self.filename = str(filename)
		fileobj = open(self.filename, "r")
		raw_list = fileobj.readlines()
		total_lines = (len(raw_list) - 1)
		
		del raw_list[total_lines]
		del raw_list[0]

		GLOB_LIST = []

		for item in raw_list:
			single_line = item.split()
			single_time = single_line[0][1:(len(single_line[0])-1)]
			single_name = single_line[1][1:(len(single_line[1])-1)]
			list_message = single_line[2:]
			single_message = " ".join(list_message)
			list_to_add = [single_time,single_name,single_message]
			GLOB_LIST.append(list_to_add)

		self.master_list = GLOB_LIST
		message_count = len(GLOB_LIST)

		last_index = int(message_count - 1)
		start_time = timedelta(seconds=int(GLOB_LIST[0][0][6:]),minutes=int(GLOB_LIST[0][0][3:5]),hours=int(GLOB_LIST[0][0][0:2]))
		end_time = timedelta(seconds=int(GLOB_LIST[last_index][0][6:]),minutes=int(GLOB_LIST[last_index][0][3:5]),hours=int(GLOB_LIST[last_index][0][0:2]))
		time_elapsed = (end_time - start_time)
		total_seconds = time_elapsed.total_seconds()
		self.total_seconds = int(total_seconds)
		messages_per_second = (float(message_count) / float(total_seconds))

		only_time_list = []

		for item in GLOB_LIST:
			new_time_obj = timedelta(seconds=int(item[0][6:]),minutes=int(item[0][3:5]),hours=int(item[0][0:2]))
			new_time_obj = int((new_time_obj - start_time).total_seconds())
			only_time_list.append(new_time_obj)

		self.only_time_list = only_time_list

	def find_spikes(self, standard_dev, human_read=False):
		if self.filename == None:
			print "No file has been loaded yet"
		else:

			#x_axis_list = range(0, int(self.total_seconds), STEP_SIZE)
			#y_axis_list = ([0] * len(x_axis_list))

			time_list = []

			for item in range((self.total_seconds + 1)):
				time_list.append(self.only_time_list.count(item))

			meanoftimes = np.mean(time_list)
			stdoftimes = np.std(time_list)

			std_dev = float(standard_dev)
			two_std = meanoftimes + (std_dev * stdoftimes)

			countindex2 = 0
			timestamplist2 = []

			for item in time_list:
				if item > two_std:
					timestamplist2.append(countindex2)
					countindex2 = countindex2 + 1
				else:
					countindex2 = countindex2 + 1

			self.spikes = timestamplist2
			finaltimelist2 = []

			for item in timestamplist2:
				minutes = int(item)/60
				secondsfor = int(item) % 60
				finalinput = str(minutes) + ":" + str(secondsfor)
				finaltimelist2.append(finalinput)

			self.human_spikes = finaltimelist2

		if human_read:
			return self.human_spikes
		elif not human_read:
			return self.spikes 


if __name__ == "__main__":
	print "Debug Mode"