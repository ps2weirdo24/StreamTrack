#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import librosa
import chat_analysis_lib

def int_to_timestamp(number_to_convert):
	raw_num = number_to_convert
	nice_min = int(raw_num/60)
	nice_sec = int(raw_num % 60)
	if nice_sec < 10:
		str_nice_sec = "0" + str(nice_sec)
		nice_time = str(nice_min) + ":" + str(str_nice_sec)
	else:
		nice_time = str(nice_min) + ":" + str(nice_sec)

	return nice_time

def average_volume(pos_list, sample_rate):
    """
    pos_list must be a list or numpy array that contains all positive values
    sample_rate is "sr" given by librosa.load()
    """
    len_raw_list = len(pos_list)
    total_numof_seconds = (int(len_raw_list)/int(sample_rate))
    list_to_pop = []
    for item in range((total_numof_seconds - 1)):
        lower_limit = int(item * sample_rate)
        higher_limit = int(((item + 1) * sample_rate) - 1)
        mean_to_add = np.mean(pos_list[lower_limit:higher_limit])
        list_to_pop.append(mean_to_add)

    return list_to_pop

def find_spikes(average_volume_list, standard_dev, human_read=False):
    avg_list = average_volume_list
    avg_vol = np.mean(avg_list)
    std_vol = np.std(avg_list)

    std_multiplier = float(standard_dev)

    threshold = avg_vol + (std_multiplier * std_vol)

    timestamplist = []
    nice_timestamp_list = []

    for item in range(len(avg_list)):
        if avg_list[item] > threshold:
            nice_min = int(item/60)
            nice_sec = int(item % 60)
            nice_time = str(nice_min) + ":" + str(nice_sec)
            timestamplist.append(int(item)+1)
            nice_timestamp_list.append(nice_time)

    if human_read:
        return nice_timestamp_list
    elif not human_read:
        return timestamplist

def clean_list(list_to_clean):
    """
    takes list of ints and removes consecutive values
    """
    value_to_remove = []
    working_list = list_to_clean

    for item in working_list:
        first_inc = item + 1
        sec_inc = item + 2
        third_inc = item + 3
        fourth_inc = item + 4
        if first_inc in working_list:
            value_to_remove.append(first_inc)
        elif sec_inc in working_list:
            value_to_remove.append(sec_inc)
        elif third_inc in working_list:
            value_to_remove.append(third_inc)
        elif fourth_inc in working_list:
            value_to_remove.append(fourth_inc)
        else:
            pass

    pre_clean = working_list
    for item in value_to_remove:
        pre_clean.remove(item)

    return pre_clean


myreader = chat_analysis_lib.ChatAnalysis()

AUDIO_PATH = "test5/trick2g.wav"
myreader.load_file("test5/trick2g.txt")

y, sr = librosa.load(AUDIO_PATH)
print "Finished importing the file.\n\n"

abs_time_series = []

for item in y:
    new_item = abs(item)
    abs_time_series.append(new_item)

final_lst = average_volume(abs_time_series, sr)

audio_spikes_low = find_spikes(final_lst, 2.25)
audio_spikes_high = find_spikes(final_lst, 3)
chat_low = myreader.find_spikes(2)
chat_high = myreader.find_spikes(5)

# print "audio low \n"
# print audio_spikes_low
# print len(audio_spikes_low)
# print "\naudio high \n"
# print audio_spikes_high
# print len(audio_spikes_high)
# print "chat low \n"
# print chat_low
# print len(chat_low)
# print "\nchat high \n"
# print chat_high
# print len(chat_high)

clean_chat_high = clean_list(chat_high)
clean_audio_high = clean_list(audio_spikes_high)

for item in clean_audio_high:
	print int_to_timestamp(item)

for item in clean_chat_high:
	print int_to_timestamp(item)

