"""

This file will be a testing ground for ways to analyze the audio portion of the stream

"""

import subprocess as sp
import os
from os import path


# orig_wav_filename = "tsm"

# temp_filename = "TEMP_info_%s.txt" % (orig_wav_filename)

# master_stat_file = "sox %s.wav -n stat 2>> %s" % (orig_wav_filename, temp_filename)

# sp.check_output(master_stat_file, shell=True)


# raw_text_file = open(temp_filename)
# list_text_file = raw_text_file.readlines()
# raw_text_file.close()
# os.remove(temp_filename)


# list_just_nums = []

# for item in list_text_file:
# 	now_split = item.split()
# 	list_just_nums.append(now_split[len(now_split)-1])


# length_seconds = int((list_just_nums[1].split("."))[0])

# print list_just_nums

"""
The above variable assignment actually works... don't touch it
"""

class AudioStats:
	def __init__(self, filename):
		self.filename = str(filename)
		self.only_filename = str((self.filename.split(".")[0])) #stripping file extension

		temp_stats_file = "TEMP_info_%s.txt" % (self.only_filename)
		call_for_stats = "sox %s -n stat 2>> %s" % (self.filename, temp_stats_file)

		sp.check_output(call_for_stats, shell=True)

		open_temp_file = open(temp_stats_file)
		file_to_list = open_temp_file.readlines()
		open_temp_file.close()
		os.remove(temp_stats_file)

		self.stats_list = []

		for item in file_to_list:
			now_split = item.split()
			self.stats_list.append(now_split[len(now_split)-1])

		self.done = True

		self.samples = self.stats_list[0]
		self.length = self.stats_list[1]
		self.max_amp = self.stats_list[3]
		self.min_amp = self.stats_list[4]
		self.midline_amp = self.stats_list[5]
		self.mean_amp = self.stats_list[7]
		self.rms_amp = self.stats_list[8]


if __name__ == "__main__":
	my_try = AudioStats("tsm.wav")
	print my_try.stats_list
