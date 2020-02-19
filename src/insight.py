import csv
import time
from datetime import datetime
import collections
import os
from decimal import Decimal, ROUND_CEILING

# read CSV file and keep the information to dt_list
dt_list = []


with open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'input/Border_Crossing_Entry_Data.csv'), mode = 'r') as file:
	reader = csv.reader(file, delimiter = ',')
	next(reader, None)
	for row in reader:
		dt_list.append(row[2:7])

# dt_list = [[Border, date, measure, value]]

# append the converted date from str to datetime format [[border, date, meausre, value]]
# create (border, measure) set
BM_list = set()
BMT_list = set()
for row in dt_list:
	time_value = time.mktime(time.strptime(row[2], '%m/%d/%Y %I:%M:%S %p'))
	row.append(time_value)
	BM_list.add((row[1],row[3]))
	BMT_list.add((time_value, row[1], row[3]))


# acc_val for this time period and cnt
BM_dic = {sets : [0,0] for sets in BM_list}

# acc_val and value and cnt
BMT_dic = {sets : [0,0,0] for sets in BMT_list}
ordered_BMT_dic = collections.OrderedDict(sorted(BMT_dic.items(), reverse = True))
# sort list by time
def sorting_time(elem):
	return float(elem[-1])
dt_list.sort(key=sorting_time)


# add up the values for same [border, measure, timevalue]
# add the 'cnt' variable for each (border, measure) for the average calculation

prev_time = 0.0
seen_BM = set()
for row in dt_list:
	cur_time = float(row[-1])
	cur_BM = (row[1], row[3])
	cur_BMT = (row[5], row[1], row[3])
	
	if cur_time > prev_time:
		seen_BM  = set()
		BM_dic[cur_BM][1] += 1
		ordered_BMT_dic[cur_BMT][2] = BM_dic[cur_BM][1]
		seen_BM.add(cur_BM)
		for k, _ in BM_dic.items():
			if prev_time != 0 and (prev_time, k[0], k[1]) in ordered_BMT_dic:

				BM_dic[(k[0], k[1])][0] += ordered_BMT_dic[((prev_time, k[0], k[1]))][0]
		prev_time = cur_time

	else:
		if cur_BM not in seen_BM:
			#fill in the cnt variable
			BM_dic[cur_BM][1] += 1
			seen_BM.add(cur_BM)
			ordered_BMT_dic[cur_BMT][2] = BM_dic[cur_BM][1]
		else:
			ordered_BMT_dic[cur_BMT][2] = BM_dic[cur_BM][1]
			
	
	ordered_BMT_dic[cur_BMT][0] += int(row[4])
	ordered_BMT_dic[cur_BMT][1] = BM_dic[cur_BM][0]

# write report.csv 
file = open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'output/report.csv'), 'w')
writer = csv.writer(file)
writer.writerow(['Border', 'Date', 'Measure', 'Value', 'Average'])
ordered_BMT_dic = collections.OrderedDict(sorted(ordered_BMT_dic.items(), reverse = True))

for key, value in ordered_BMT_dic.items():
	try:
		writer.writerow([key[1], datetime.fromtimestamp(float(key[0])).strftime('%m/%d/%Y %I:%M:%S %p'), key[2], value[0], Decimal(str(value[1]/(value[2]-1))).quantize(0, ROUND_CEILING)])
	# if calculating the average of first month, just fill in 0
	except ZeroDivisionError:
		writer.writerow([key[1], datetime.fromtimestamp(float(key[0])).strftime('%m/%d/%Y %I:%M:%S %p'), key[2], value[0], 0])

file.close()