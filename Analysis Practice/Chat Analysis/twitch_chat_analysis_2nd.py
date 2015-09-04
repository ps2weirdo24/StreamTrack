# This script will take a text file of twitch chat and provide some stats
# and other helpful information for selecting noteworthy clips

from datetime import timedelta
import matplotlib.pyplot as plt

raw_file = open("sample_chat.txt")

raw_list = raw_file.readlines()

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

	

"""

By this point in the script GLOB_LIST has been created and populated with lists that contain 3 strings,

time message was entered [HH:MM:SS] , username of sender and finally the message.

"""

message_count = len(GLOB_LIST)

last_index = int(message_count - 1)

start_time = timedelta(seconds=int(GLOB_LIST[0][0][6:]),minutes=int(GLOB_LIST[0][0][3:5]),hours=int(GLOB_LIST[0][0][0:2]))

end_time = timedelta(seconds=int(GLOB_LIST[last_index][0][6:]),minutes=int(GLOB_LIST[last_index][0][3:5]),hours=int(GLOB_LIST[last_index][0][0:2]))

time_elapsed = (end_time - start_time)

total_seconds = time_elapsed.total_seconds()

messages_per_second = (float(message_count) / float(total_seconds))

only_time_list = []

for item in GLOB_LIST:
	new_time_obj = timedelta(seconds=int(item[0][6:]),minutes=int(item[0][3:5]),hours=int(item[0][0:2]))
	new_time_obj = int((new_time_obj - start_time).total_seconds())
	only_time_list.append(new_time_obj)

""" Next I will focus on plotting the points and changing things like step size and starting points """

STEP_SIZE = 7

x_axis_list = range(0, message_count, STEP_SIZE)

y_axis_list = ([0] * len(x_axis_list))

lower_limit = 0
higher_limit = 4
adding_index = 0

for item in only_time_list:
	if (item >= lower_limit) and (item <= higher_limit):
		y_axis_list[adding_index] += 1
	elif (item >= higher_limit):
		adding_index += 1
		lower_limit += STEP_SIZE
		higher_limit += STEP_SIZE
		if adding_index <= (len(y_axis_list) - 1):
			y_axis_list[adding_index] += 1
		else:
			break
	else:
		print "oops"


plt.plot(x_axis_list, y_axis_list)

plt.show()

print "DONE"

# time_delta_1 = timedelta(seconds=int(example_time_1[6:]),minutes=int(example_time_1[3:5]),hours=int(example_time_1[0:2]))
# time_delta_2 = timedelta(seconds=int(example_time_2[6:]),minutes=int(example_time_2[3:5]),hours=int(example_time_2[0:2]))
