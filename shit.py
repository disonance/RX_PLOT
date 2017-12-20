#!/usr/bin/env python
import re
import sys

filename = '/Users/dennisngsze_yang/Desktop/N84_Data_RX/ca_coverage.txt'
f1 = open(filename, "rU")
f2 = open('/Users/dennisngsze_yang/Desktop/N84_Data_RX/ca_coverage_output.txt', "w+")
orig_stdout = sys.stdout
sys.stdout = f2

nof_lines = 0
read_from_here = 0
path_idx = 0
catest_list = []
port_list = []
ca_port_a_combo_list = []
port_test_list = []


class idx(object):
    def __init__(self, idx, pcc_port, scc1_port, scc2_port, scc3_port):
        self.idx = idx
        self.pcc_port = pcc_port
        self.scc1_port = scc1_port
        self.scc2_port = scc2_port
        self.scc3_port = scc3_port


class ca(object):
    def __init__(self, cc_type, tech, port, pcc_rx_, scc1_rx_, scc2_rx_, scc3_rx_, path_idx, ca_combo):
        self.cc_type = cc_type
        self.tech = tech
        self.port = port
        self.pcc_rx_test = pcc_rx_
        self.scc1_rx_test = scc1_rx_
        self.scc2_rx_test = scc2_rx_
        self.scc3_rx_test = scc3_rx_
        self.path_idx = path_idx
        self.ca_combo = ca_combo


class ca_port_test(object):
    def __init__(self, idx, port, pcc_rx, scc1_rx, scc2_rx, scc3):
        self.idx = idx
        self.port = port
        self.pcc_rx = pcc_rx
        self.scc1_rx = scc1_rx
        self.scc2_rx = scc2_rx
        self.scc3_rx = scc3_rx


def rx_decode(rx_test):
    i = int(rx_test, base=2)
    str = ""
    check = 0;
    for x in range(0, 4):
        if (i & (0b1000 >> x)):
            if check == 0:
                str += "TEST_RX"
                check = 1
            str += ("%d" % x)
            #     r_str = ",".join(str)
    return str


def band40_patch_check(project, port, rx_enable, band_group):
    enable = 0
    # print rx_enable
    if (project == "D3X"):
        if port == "A" and (rx_enable.find("2") != -1 or rx_enable.find("3") != -1):
            # print "Port A Rx2/Rx3 true"
            enable = 1
        elif port == "B" and (rx_enable.find("2") != -1 or rx_enable.find("3") != -1):
            # print "Port A Rx2/Rx3 true"
            enable = 1
        elif port == "C":
            # print "Port C"
            enable = 1
        elif port == "D":
            # print "Port D"
            enable = 1
        else:
            enable = 0
    elif (project == "N84"):
        if port == "A" and (rx_enable.find("1") != -1):
            # print "Port A Rx2/Rx3 true"
            enable = 1
        elif port == "B" and (rx_enable.find("0") != -1):
            # print "Port A Rx2/Rx3 true"
            enable = 1
        else:
            enable = 0

    else:
        enable = 0

    return enable


def print_structure(path_idx, port, pcc_rx_test, scc1_rx_test, scc2_rx_test, scc3_rx_test, ca_combo, sku, project):
    ca_bands = catest_list[x].ca_combo[4:].split("_", 4)
    component_carrier = []
    band_group = []
    band_group_temp = []
    mimo_enable = []
    sawless_enable = []
    mimo_print = ["", "_MIMO"]
    filterless_print = ["", "_FILTERLESS"]
    rx_enable = [rx_decode(pcc_rx_test), rx_decode(scc1_rx_test), rx_decode(scc2_rx_test), rx_decode(scc3_rx_test)]
    string = ""
    mimo_enable_disable = ["MIMO_DISABLE", "MIMO_ENABLE"]
    filtered_disable = ["NORMAL_PATH", "FILTERLESS_PATH"]
    for count in range(0, len(ca_bands)):
        if ca_bands[count].find("Filterless (MIMO)") != -1:
            sawless_enable.append(1);
            mimo_enable.append(1);
            component_carrier = ca_bands[count].split(" ")
            test_var = component_carrier[0]
            band_number = test_var[1:]
            band_group.append(band_number)
        elif ca_bands[count].find("MIMO") != -1:
            mimo_enable.append(1);
            sawless_enable.append(0);
            component_carrier = ca_bands[count].split(" ")
            test_var = component_carrier[0]
            band_number = test_var[1:]
            band_group.append(band_number)
        elif ca_bands[count].find("Filterless") != -1:
            sawless_enable.append(1);
            mimo_enable.append(0);
            component_carrier = ca_bands[count].split(" ")
            test_var = component_carrier[0]
            band_number = test_var[1:]
            band_group.append(band_number)
        else:
            mimo_enable.append(0);
            sawless_enable.append(0);
            test_var = ca_bands[count]
            band_number = test_var[1:]
            band_group.append(band_number)

    band_40A_force = 0
    for freq_count in range(0, len(ca_bands)):
        if (band_group[freq_count] == "40") and band_40A_force == 0:
            band_40A_force = band40_patch_check(project, port, rx_enable[freq_count], band_group[freq_count]);

    string = "\t[DL_CA_"
    for freq_count in range(0, len(ca_bands)):
        band_group_new = band_group[freq_count];
        if (band_40A_force == 1 and band_group[freq_count] == "40"):
            band_group_new = "40A"
        else:
            band_group_new = band_group[freq_count];
        string = string + "B" + band_group_new + filterless_print[sawless_enable[freq_count]] + mimo_print[
            mimo_enable[freq_count]]
        if freq_count < (len(ca_bands) - 1):
            string = string + "_"
    string = string + "] ="
    print string
    print "\t{\n\t\t.ca_meas_state =\n\t\t1,\n\t\t.band_component=\n\t\t{"

    string = ""
    channel_string = "_UL_MID_CH_D101, "
    print "\t\t\t // Band, Tx Meas Enable, Rx Path Meas Bitmask, MIMO flag, Filterless flag, UL ch, DL Ch, BW, UL config when test PCC Rx, UL config when test SCC Rx"

    for freq_count in range(0, len(ca_bands)):
        if rx_enable[freq_count] == "":
            rx_enable[freq_count] = "0";
        if ((freq_count > 0) and (band_group[freq_count] == band_group[freq_count - 1])):
            channel_string = "_UL_HIGH_CH_D101, "
        elif ((freq_count < (len(ca_bands) - 1)) and (band_group[freq_count] == band_group[freq_count + 1])):
            channel_string = "_UL_LOW_CH_D101, "
        else:
            channel_string = "_UL_MID_CH_D101, "
        # special handling for Band 29
        if (band_group[freq_count] == "29"):
            channel_string = "_DL_MID_CH_D101, "

        band_group_new = band_group[freq_count];
        if (band_40A_force == 1 and band_group[freq_count] == "40"):
            band_group_new = "40A"
        else:
            band_group_new = band_group[freq_count];

        if freq_count == 0:  # PCC
            start_rb, no_of_rb = return_tx_config(band_group[freq_count]);
            string = string + "\t\t\t{ LTE_FrequencyBand_" + band_group_new + ", 0, " + rx_enable[freq_count] + ", " + \
                     mimo_enable_disable[mimo_enable[freq_count]] + ", " + filtered_disable[sawless_enable[
                freq_count]] + ", LTE_B" + band_group_new + channel_string + "0, LTE_BW_10_0MHz, LTE_TX_UL_CONFIG_QPSK_" + str(
                start_rb) + "_" + str(
                no_of_rb) + ", LTE_TX_UL_CONFIG_QPSK_0_50" + ", LTE_TX_UL_CONFIG_QPSK_0_50" + ", LTE_TX_UL_CONFIG_QPSK_0_50" + "},"
        else:  # SCELL's
            string = string + "\n\t\t\t{ LTE_FrequencyBand_" + band_group_new + ", 0, " + rx_enable[freq_count] + ", " + \
                     mimo_enable_disable[mimo_enable[freq_count]] + ", " + filtered_disable[sawless_enable[
                freq_count]] + ", LTE_B" + band_group_new + channel_string + "0, LTE_BW_10_0MHz" + "},"
    for freq_count in range(len(ca_bands), 5):
        string = string + "\n\t\t\t{ LTE_FrequencyBand_INVALID },"
    print string

    print "\t\t},"
    print "\n\t\t.japan_or_row=\n\t\t" + sku + "\n\t},"


def return_tx_config(band):
    # Uplink config for each band
    pcc_band = ["1", "2", "3", "4", "5", "7", "8", "11", "12", "13", "14", "17", "18", "19", "20", "21", "25", "26",
                "28", "30", "34", "38", "39", "40", "40A", "41", "42", "66", "71A", "71B"]
    start_rb = [0, 0, 0, 0, 25, 0, 25, 25, 30, 0, 0, 30, 25, 25, 0, 25, 0, 25, 25, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    rb = [50, 50, 50, 50, 25, 50, 25, 25, 20, 20, 15, 20, 25, 25, 20, 25, 50, 25, 25, 25, 50, 50, 50, 50, 50, 50, 50,
          50, 20, 20];

    ret_start_rb = ""
    ret_rb = ""
    for count in range(0, len(pcc_band)):
        if (band == pcc_band[count]):
            ret_start_rb = start_rb[count]
            ret_rb = rb[count];
    return ret_start_rb, ret_rb


for line in f1:
    if "PROJECT" in line:
        project = re.search('\S+', line[11:])
        print project.group()
    if "SKU" in line:
        sku = re.search('\S+', line[7:])
    if "CA_START" in line:
        read_from_here = 1
        continue
    if "CA_END" in line:
        break
    if read_from_here:
        # print line
        path_idx = re.search('\d+', line)
        tech = re.search('\S+', line[27:])
        ca_combo = re.search("\S+.*", line[27:])
        pcc_port = re.search('\S', line[7:])
        pcc_rx = rx = re.search('\d+', line[8:])
        scc1_port = re.search('\S', line[12:])
        scc1_rx = rx = re.search('\d+', line[13:])
        scc2_port = re.search('\S', line[17:])
        scc2_rx = rx = re.search('\d+', line[18:])
        scc3_port = re.search('\S', line[22:])
        scc3_rx = rx = re.search('\d+', line[23:])

        catest_list.append(
            ca("pcc", tech.group(), pcc_port.group(), pcc_rx.group(), scc1_rx.group(), scc2_rx.group(), scc3_rx.group(),
               path_idx.group(), ca_combo.group()))
        # print pcc_port.group()
        pcc_port_s = pcc_port.group()
        scc1_port_s = scc1_port.group()
        scc2_port_s = scc2_port.group()
        scc3_port_s = scc3_port.group()

        if (pcc_rx.group() == "0000"):
            pcc_port_s = ""
        if (scc1_rx.group() == "0000"):
            scc1_port_s = ""
        if (scc2_rx.group() == "0000"):
            scc2_port_s = ""
        if (scc3_rx.group() == "0000"):
            scc3_port_s = ""

        port_list.append(idx(path_idx.group(), pcc_port_s, scc1_port_s, scc2_port_s, scc3_port_s))

print len(catest_list)
# in the event PCC & SCC bands are of differnt port.
print "Checking list"
for x in range(0, len(port_list)):
    port_test_list.append(port_list[x].pcc_port)
    port_test_list.append(port_list[x].scc1_port)
    port_test_list.append(port_list[x].scc2_port)
    port_test_list.append(port_list[x].scc3_port)

    if (len(set(port_test_list)) > 2):
        state = ' ERROR!'
    else:
        state = ' OK!'

    print ("Path Idx %s" % port_list[x].idx) + " " + port_list[x].pcc_port + port_list[x].scc1_port + port_list[
        x].scc2_port + port_list[x].scc3_port + state
    # print port_test_list
    port_test_list[:] = []
    # if catest_list[x].port == 'A' and catest_list[x].cc_type == 'pcc' and catest_list[x].rx_test != '0000':
    #     print "PCC\t" + catest_list[x].path_idx + " " +  catest_list[x].port + catest_list[x].rx_test + " -> " + catest_list[x].ca_combo
print "//Port A"
print "{"
for x in range(0, len(catest_list)):
    if catest_list[x].tech == 'LTE':
        if catest_list[x].port == 'A' and (
                        catest_list[x].pcc_rx_test != '0000' or catest_list[x].scc1_rx_test != '0000' or catest_list[
                x].scc2_rx_test != '0000' or catest_list[x].scc3_rx_test != '0000'):
            print_structure(catest_list[x].path_idx, catest_list[x].port, (catest_list[x].pcc_rx_test),
                            (catest_list[x].scc1_rx_test), (catest_list[x].scc2_rx_test), (catest_list[x].scc3_rx_test),
                            catest_list[x].ca_combo, sku.group(), project.group())
print "\n};"

print "//Port B"
print "{"
for x in range(0, len(catest_list)):
    if catest_list[x].tech == 'LTE':
        if catest_list[x].port == 'B' and (
                        catest_list[x].pcc_rx_test != '0000' or catest_list[x].scc1_rx_test != '0000' or catest_list[
                x].scc2_rx_test != '0000' or catest_list[x].scc3_rx_test != '0000'):
            print_structure(catest_list[x].path_idx, catest_list[x].port, (catest_list[x].pcc_rx_test),
                            (catest_list[x].scc1_rx_test), (catest_list[x].scc2_rx_test), (catest_list[x].scc3_rx_test),
                            catest_list[x].ca_combo, sku.group(), project.group())
print "\n};"

print "//Port C"
print "{"
for x in range(1, len(catest_list)):
    if catest_list[x].tech == 'LTE':
        if catest_list[x].port == 'C' and (
                        catest_list[x].pcc_rx_test != '0000' or catest_list[x].scc1_rx_test != '0000' or catest_list[
                x].scc2_rx_test != '0000' or catest_list[x].scc3_rx_test != '0000'):
            print_structure(catest_list[x].path_idx, catest_list[x].port, (catest_list[x].pcc_rx_test),
                            (catest_list[x].scc1_rx_test), (catest_list[x].scc2_rx_test), (catest_list[x].scc3_rx_test),
                            catest_list[x].ca_combo, sku.group(), project.group())
print "\n};"

print "//Port D"
print "{"
for x in range(0, len(catest_list)):
    if catest_list[x].tech == 'LTE':
        if catest_list[x].port == 'D' and (
                        catest_list[x].pcc_rx_test != '0000' or catest_list[x].scc1_rx_test != '0000' or catest_list[
                x].scc2_rx_test != '0000' or catest_list[x].scc3_rx_test != '0000'):
            print_structure(catest_list[x].path_idx, catest_list[x].port, (catest_list[x].pcc_rx_test),
                            (catest_list[x].scc1_rx_test), (catest_list[x].scc2_rx_test), (catest_list[x].scc3_rx_test),
                            catest_list[x].ca_combo, sku.group(), project.group())
print "\n};"

sys.stdout = orig_stdout
f2.close()
