## Read CSV
I used os package to find the parent directory of the file and enter the input file to read the CSV.
After reading the CSV file, store the only information I need (Border, date, measure, value) into dt_list
dt_list = [[Border, date, measure, value]]

## Create Border_Measure dictionary and Border_Measure_Time dictionary
1.BM_list contains sets of (Border, Measure) while BMT_list contains sets of (Date, Border, Measure)
By using BM_list and BMT_list, create BM_dic which stores [values for a certain month, the count of the month before this period], and BMT_dic which stores [values for a certain month, accumulated values before this period, the count of the month before this period]]

2.sort BMT_dic by ascending date. Store as ordered_BMT_dic

## Fill in ordered_BMT_dic
initialize some variables (prev_time, seen_BM) before the for loop.

for each row in dt_list, save the current status (cur_time, cur_BM, cur_BMT) 
if the time has moved to the next period:
    reset seen_BM and (count of the month+1)
    using the prev_time to get the values of previous timestamp for certain BM, and add it to the 
    
    
## Export the ordered_BMT_dic to CSV
write the CSV from ordered_BMT_dic into the output file.

## Running instruction
Just run the insight.py in src folder
