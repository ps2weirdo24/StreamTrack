import chat_analysis_lib

chatreader = chat_analysis_lib.ChatAnalysis()

chatreader.loadfile("flosd_1842-1902.txt")

print chatreader.only_time_list

# spike_list = chatreader.find_spikes(15, 2.1)
# outlier_spike_list = chatreader.find_spikes(10, 3)
# print spike_list
# print outlier_spike_list


print "Done"
