#!/usr/local/bin/python
import csv
import re
import Tkinter
import numpy as np
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool,BoxZoomTool,ResetTool ,PanTool,BoxSelectTool
import bokeh.palettes
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.layouts import widgetbox
from bokeh.layouts import layout
from time import sleep

# from bokeh.palettes  import Category20

# print bokeh.palettes.Category20

output_file("line.html")

#filename = raw_input("Input File - > ")
filename ='/Users/dennisngsze_yang/Desktop/N84_Data_RX/Cellular Station 3_ROW_2017-12-16_16-23-35.csv'

search_str_input = raw_input("Search Str ->")
# upper_limit = raw_input("Upper Limit ->")
# lower_limit = raw_input("Lower Limit ->")
f1 = open(filename, "rU")
f2 = open("applepass_list.txt","w+")
f3 = open(search_str_input+".txt","w+")

f1.readline()
reader = csv.DictReader(f1)
search_fieldlist = []
data = []
upper_limit = []
lower_limit = []
apple_pass_upper_limit = []
apple_pass_lower_limit = []
header = reader.fieldnames
search_str_list = []
test_list = []
x_range = []
# for level in range (1,7):
#     search_str_list.append ("LTE.*RSSI Level " + str(level))
#
# print (search_str_list)

hover = HoverTool(tooltips=[
        ("index", "$index"),
        ("Power", "@y"),
        ("desc", "@desc"),
    ],
    names=["foo"],
    mode='vline'
    )

hover.point_policy = "snap_to_data"
hover.line_policy = "nearest"
p = figure(plot_width=800, plot_height=800, title="LTE RSSI",
               tools=[hover, BoxZoomTool(), ResetTool(), PanTool(),BoxSelectTool()])

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

        BBFW = row['BB_FIRMWARE_VERSION'];
        # if row['Test Pass/Fail Status'] =='Error':
        #     continue

        # if row['Test Pass/Fail Status'] == 'Fail':
        #     continue

        for field in search_fieldlist:
            if row[field] == 'NA':
                continue

            # data.append(round(float(row[field]),3))
            data.append(float(row[field]))
            print (row[field])

        print ("nof of data " , len(data))
    print (len(data)/len(search_fieldlist))

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

    print (len(data_array_split))
    print (upper_limit_split[0])

    for i in range(len(apple_pass_upper_limit_split[0])):
        if i == 77:
            print "here", apple_pass_upper_limit_split[0][i]
        if apple_pass_upper_limit_split[0][i] == 'NA':
            apple_pass_upper_limit_split[0][i] = np.nan
    for i in range(len(apple_pass_lower_limit_split[0])):
        if apple_pass_lower_limit_split[0][i] == 'NA':
            apple_pass_lower_limit_split[0][i] = np.nan

    fig = plt.figure(1).canvas.set_window_title("LTE RSSI" + filename + BBFW)
    x=320 + level
    plt.subplots_adjust(hspace=.5)

    fig = plt.subplot(x)
    plt.title(search_str)
    plt.plot(upper_limit_split[0],color='r')
    plt.plot(lower_limit_split[0],color='r')
    plt.plot(apple_pass_upper_limit_split[0],color='y')
    plt.plot(apple_pass_lower_limit_split[0],color='y')


    test_list = range(len(search_fieldlist))


    source1 = ColumnDataSource(data=dict(
        y=upper_limit_split[0],
        x=test_list,
        desc=search_fieldlist

    ))

    source2 = ColumnDataSource(data=dict(
        y=lower_limit_split[0],
        x=test_list,
        desc=search_fieldlist

    ))
    source3 = ColumnDataSource(data=dict(
        y=apple_pass_upper_limit_split[0],
        x=test_list,
    ))

    source4 = ColumnDataSource(data=dict(
        y=apple_pass_lower_limit_split[0],
        x=test_list,
    ))

    p.line("x", "y", source=source1, color="red", line_width=3)
    p.line("x", "y", name="foo1", source=source2, color="red", line_width=3)
    # p.line("x", "y", source=source3, color="orange", line_width=3)
    # p.line("x", "y", source=source4, color="orange", line_width=3)

    columns = [
    TableColumn(field="desc", title='Desc'),
    ]




    # show(p)
    # mypalette = magma[0:len(data)/len(search_fieldlist)]
    x = 0
    for i in range(0,len(data)/len(search_fieldlist)):
        # plt.plot(data_array_split[i],range(len(search_fieldlist)))
        plt.plot( range(len(search_fieldlist)),data_array_split[i])

        source = ColumnDataSource(data=dict(
            y=data_array_split[i],
            x=test_list,
            desc=search_fieldlist
        ))
        x = x + 1
        if (i == 0):
            p.line("x", "y", name="foo", color = bokeh.palettes.Category20[20][x], source=source, line_width=1)
        else:
            p.line("x", "y", name="Boo", color = bokeh.palettes.Category20[20][x], source=source, line_width=1)
        if x == 17:
            x = 0
        # p.circle("x", "y", source=source, size=1, color="red")
        # p.line("x", "y", source=source,name = "foo", color="blue", line_width=1)
    data_table = DataTable(source=source, columns=columns, width=1000, height=500)

    #show(p)
    # show(widgetbox(data_table))

    l = layout([
        p, widgetbox(data_table),


    ])
    show(l)

    # for i in range(0,len(data)/len(search_fieldlist)):
    #
    #     for y in range(0, len(data_array_split[i])):
    #         if (data_array_split[i][y] > upper_limit_split[0][y]):
    #             f3.write(search_fieldlist[y] + 'data ' + str(data_array_split[i][y]) + ' limit ' + str(upper_limit_split[0][y]) + '\r\n')
    #         if (data_array_split[i][y] < lower_limit_split[0][y]):
    #             f3.write(search_fieldlist[y] + 'data ' + str(data_array_split[i][y]) + ' limit ' + str(lower_limit_split[0][y]) + '\r\n')
    #
    #     f3.write('\r\n')

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
    # lines = plt.plot(range(10), 'o')
plt.show()











