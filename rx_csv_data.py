import csv
import re
import numpy as np

filename ='/Users/dennisngsze_yang/Desktop/N84_Data_Rx/Cellular Station 1P_ROW_2017-12-16_15-11-11.csv'

search_str_input = raw_input("Search Str ->")
# upper_limit = raw_input("Upper Limit ->")
# lower_limit = raw_input("Lower Limit ->")
mp_delta = 0
f1 = open(filename, "rU")
f2 = open("MP_Failure.txt","w+")
f3 = open("Apple_Pass.txt","w+")
f4 = open("External_Data_MP_Failure.txt","w+")
f5 = open("External_Data_Apple_Pass.txt","w+")
f5 = open("External_Data_MP_03.txt","w+")
f1.readline()

reader = csv.DictReader(f1)
search_fieldlist = []
serial_number_array = []
data = []

upper_limit = []
lower_limit = []
apple_pass_upper_limit = []
apple_pass_lower_limit = []
header = reader.fieldnames
search_str_list = []
test_list = []
x_range = []
failure_items=[]
ordered_failure_items = []
risk_failure_items = []
ordered_risk_failure_items = []

for row in reader:

    if row['Product'] == "Upper Limits----->":
        for field in search_fieldlist:
            upper_limit.append(float(row[field]))

    if row['Product'] == "Lower Limits----->":
        for field in search_fieldlist:
            lower_limit.append(float(row[field]))

    if row['Product'] == "Apple Pass Upper Limits----->":
        for field in search_fieldlist:
            apple_pass_upper_limit.append(float(row[field]))

    if row['Product'] == "Apple Pass Lower Limits----->":
        for field in search_fieldlist:
            apple_pass_lower_limit.append(float(row[field]))


# for i in range(len(apple_pass_lower_limit)):
#     f2.write(field + ' ' + upper_limit[i] + lower_limit[i] + '\r\n')

search_fieldlist[:] = []


for level in range (1,7):
    search_str = search_str_input +".*RSSI Level "+ str(level)
    print (search_str)
    for field in header:
        #f2.write(field + '\r\n' )
        mdata = re.search(search_str,field)

        if mdata:
     #       print field
            search_fieldlist.append(field)
    print ("nof of fields",len(search_fieldlist))
    if(len(search_fieldlist))==0:
        print ("no fields found")
        break



    f1.seek(0)
    f1.readline()
    reader = csv.DictReader(f1)

    for row in reader:

        if row['Product'] == "Upper Limits----->":
            for field in search_fieldlist:
                if(row[field] == 'NA'):
                    upper_limit.append(np.nan)
                else:
                    upper_limit.append(float(row[field]))

        if row['Product'] == "Lower Limits----->":
            for field in search_fieldlist:
                if(row[field] == 'NA'):
                    lower_limit.append(np.nan)
                else:
                    lower_limit.append(float(row[field]))

        if row['Product'] == "Apple Pass Upper Limits----->":
            for field in search_fieldlist:
                if(row[field] == 'NA'):
                    apple_pass_upper_limit.append(np.nan)
                else:
                    apple_pass_upper_limit.append(float(row[field]))

        if row['Product'] == "Apple Pass Lower Limits----->":
            for field in search_fieldlist:
                if(row[field] == 'NA'):
                    apple_pass_lower_limit.append(np.nan)
                else:
                    apple_pass_lower_limit.append(float((row[field])))

        if row['SerialNumber'] == '':
            continue
        else:
            serial_number = row['SerialNumber']
            serial_number_array.append(serial_number)
            # f2.write(serial_number +'\r\n')

        for field in search_fieldlist:
            if row[field] == 'NA':
                continue

            # data.append(round(float(row[field]),3))
            data.append(float(row[field]))
            # print (row[field])

        print ("nof of data " , len(data))
    print (len(data)/len(search_fieldlist))

    #handle Combined CSVs
    if (len(data)/len(search_fieldlist) >0):
        data_array_split = np.array_split(data, len(data)/len(search_fieldlist))
        upper_limit_split = np.array_split(upper_limit, len(upper_limit)/len(search_fieldlist))
        lower_limit_split = np.array_split(lower_limit, len(lower_limit)/len(search_fieldlist))
        apple_pass_upper_limit_split = np.array_split(apple_pass_upper_limit, len(apple_pass_upper_limit) / len(search_fieldlist))
        apple_pass_lower_limit_split = np.array_split(apple_pass_lower_limit, len(apple_pass_lower_limit) / len(search_fieldlist))
    else:
        data_array_split = data
        upper_limit_split = upper_limit
        lower_limit_split = lower_limit
        apple_pass_upper_limit_split = apple_pass_upper_limit
        apple_pass_lower_limit_split = apple_pass_lower_limit

    for i in range(len(apple_pass_upper_limit_split[0])):
        if apple_pass_upper_limit_split[0][i] == 'NA':
            apple_pass_upper_limit_split[0][i] = np.nan
    for i in range(len(apple_pass_lower_limit_split[0])):
        if apple_pass_lower_limit_split[0][i] == 'NA':
            apple_pass_lower_limit_split[0][i] = np.nan


    test_list = range(len(search_fieldlist))

    for cnt in range(0,len(data)/len(search_fieldlist)):
        f2.write('[' + serial_number_array[cnt] + ']' + 'level '+ str(level) +'\r\n')
        f3.write('[' + serial_number_array[cnt] + ']' + 'level '+ str(level) +'\r\n')

        for item_no in range(0,len(search_fieldlist)):
            if data_array_split[cnt][item_no] > upper_limit_split[0][item_no] or data_array_split[cnt][item_no] < lower_limit_split[0][item_no]:
                print '['+ serial_number_array[cnt] +']' + ' ' + search_fieldlist[item_no]
                f2.write (search_fieldlist[item_no]+'\r\n')

        for item_no in range(0,len(search_fieldlist)):
            if data_array_split[cnt][item_no] > apple_pass_upper_limit_split[0][item_no] or data_array_split[cnt][item_no] < apple_pass_lower_limit_split[0][item_no]:
                print '['+ serial_number_array[cnt] +']' + ' ' + search_fieldlist[item_no]
                f3.write (search_fieldlist[item_no]+'\r\n')
        f2.write ('\r\n')
        f3.write ('\r\n')

    for cnt in range(0, len(data) / len(search_fieldlist)):

        for item_no in range(0, len(search_fieldlist)):
            if data_array_split[cnt][item_no] > (upper_limit_split[0][item_no] + mp_delta) or data_array_split[cnt][item_no] < \
                    (lower_limit_split[0][item_no]- mp_delta):
                print '[' + serial_number_array[cnt] + ']' + ' ' + search_fieldlist[item_no]
                failure_items.append(search_fieldlist[item_no])

        for item_no in range(0, len(search_fieldlist)):
            if data_array_split[cnt][item_no] > (upper_limit_split[0][item_no]-0.3) or data_array_split[cnt][item_no] < \
                    (lower_limit_split[0][item_no]+0.3):
                print '[' + serial_number_array[cnt] + ']' + ' ' + search_fieldlist[item_no]
                risk_failure_items.append(search_fieldlist[item_no])

        f2.write('\r\n')
        f3.write('\r\n')


    search_fieldlist[:] = []
    data[:] = []
    data_array_split[:] = []
    upper_limit_split[:] = []
    apple_pass_lower_limit_split[:] = []
    apple_pass_upper_limit_split[:] = []
    lower_limit[:] = []
    upper_limit[:] = []
    apple_pass_lower_limit[:] = []
    apple_pass_upper_limit[:] = []

ordered_failure_items = list(set(failure_items))
ordered_risk_failure_items = list(set(risk_failure_items))

for x in range(0,len(ordered_failure_items)):
    f4.write( ordered_failure_items[x] +'\r\n')

for x in range(0,len(ordered_risk_failure_items)):
    f5.write( ordered_risk_failure_items[x] +'\r\n')



f1.close()
f2.close()
f3.close()
f4.close()
f5.close()