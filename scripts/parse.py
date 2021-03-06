#!/usr/bin/python2

import csv
import getopt
import sys
import xml.etree.cElementTree as ET

provinces_dict = {}
regencies_dict = {}
districts_dict = {}
villages_dict = {}

def read_html_data(fname):
    print 'Reading html data...'
    with open(fname, 'rb') as inputfile:
        append = False
        for line in inputfile:
            if '<tr class="table_content">' in line:
                inputbuffer = line
                append = True
            elif '</tr>' in line:
                if append:
                    inputbuffer += line
                    append = False
                    process_buffer(inputbuffer)
                    inputbuffer = ''
            elif append:
                inputbuffer += line

def process_buffer(buf):
    tnode = ET.fromstring(buf)
    print tnode[0].text.strip()
    province_id = tnode[1].text.strip()
    province_name = tnode[2].text.strip()
    regency_id = province_id + tnode[3].text.strip()
    regency_name = tnode[4].text.strip()
    district_id = regency_id + tnode[5].text.strip()
    district_name = tnode[6].text.strip()
    village_id = district_id + tnode[7].text.strip()
    village_name = tnode[8].text.strip()

    provinces_dict[province_id] = province_name
    regencies_dict[regency_id] = regency_name
    districts_dict[district_id] = district_name
    villages_dict[village_id] = village_name

def write_data_to_csv():
    print 'Writing provinces data...'
    write_dict_to_csv('../csv/provinces.csv', provinces_dict)
    print 'Writing regencies data...'
    write_dict_to_csv('../csv/regencies.csv', regencies_dict, 2)
    print 'Writing districts data...'
    write_dict_to_csv('../csv/districts.csv', districts_dict, 5)
    print 'Writing villages data...'
    write_dict_to_csv('../csv/villages.csv', villages_dict, 7)
    print 'Done.'

def write_dict_to_csv(fname, data_dict, prev_key_length = 0):
    with open(fname, 'wb') as fp:
        fcsv = csv.writer(fp, delimiter=',')
        if prev_key_length > 0:
            for key, value in sorted(data_dict.iteritems()):
                fcsv.writerow([key, key[:prev_key_length], value])
        else:
            for key, value in sorted(data_dict.iteritems()):
                fcsv.writerow([key, value])

def main(argv):
    if (len(argv) == 1):
        read_html_data(argv[0])
        write_data_to_csv()
    else:
        print "usage: parse.py <html_input_file>"
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])