#!/usr/bin/python

# This script is used to read a file of item xml data that is the batch report output from the Aleph service ret-adm-03
# and then generate a matrix of all the variant combinations of sublibraries, collections, material types, and item statuses
# with a count of items for each combination.

import codecs
import re
import sys

filename_path = raw_input('Enter the relative filename path for the item xml you want to analyze: ')

# INPUT FILE(S)
items_xml_file = codecs.open(filename_path,'r')
items_xml_str = items_xml_file.read()
items_xml_file.close()

# split the string of item record xml data into separate elements representing each item based on the XML delimiter <section-02>
item_rec_delim_re = re.compile(r'<section-02>')
item_recs = re.split(item_rec_delim_re, items_xml_str)
item_recs.pop(0)	# remove the first element in the list which reflects the header fields of the XML document

# OUTPUT FILE(S)
item_matrix_out = codecs.open(filename_path+'_matrix.txt','w')

#############################################################
##  Method:  build_item_matrix()
#############################################################
def build_item_matrix(item_rec, matrix_dict):
	xml_close_tag_re = re.compile(r'</.*>')
	item_rec_lines = item_rec.split('\n')
	for item_rec_line in item_rec_lines:
		if item_rec_line.startswith('<z30-sub-library>'):
			sublibrary = item_rec_line[17:]
			sublibrary = re.split(xml_close_tag_re, sublibrary)[0]
		
		if item_rec_line.startswith('<z30-collection>'):
			collection = item_rec_line[16:]
			collection = re.split(xml_close_tag_re, collection)[0]
		
		if item_rec_line.startswith('<z30-material>'):
			material = item_rec_line[14:]
			material = re.split(xml_close_tag_re, material)[0]
		
		if item_rec_line.startswith('<z30-item-status>'):
			item_status = item_rec_line[17:]
			item_status = re.split(xml_close_tag_re, item_status)[0]
		
		if item_rec_line.startswith('<z30-item-process-status>'):
			ips = item_rec_line[25:]
			ips = re.split(xml_close_tag_re, ips)[0]
		
		if item_rec_line.startswith('<z30-temp-location>'):
			temp_loc = item_rec_line[19:]
			temp_loc = re.split(xml_close_tag_re, temp_loc)[0]
	
	matrix_key = sublibrary+'|'+collection+'|'+material+'|'+item_status+'|'+ips+'|'+temp_loc
	
	matrix_dict[matrix_key] = matrix_dict.get(matrix_key, 0) + 1
	
	return matrix_dict



item_matrix_dict = dict()
num_item_recs_processed = 0
for item_rec in item_recs:
	item_matrix_dict = build_item_matrix(item_rec, item_matrix_dict)
	num_item_recs_processed += 1
	status_text = '\rProcessed: {0:,} of {1:,} items'.format(num_item_recs_processed, len(item_recs))
	sys.stdout.write(status_text)
	sys.stdout.flush()


item_matrix_out.write('Sublibrary|Collection|Material Type|Item Status|IPS|Temp Loc|Item Count\n')
for key, count in item_matrix_dict.iteritems():
	item_matrix_out.write(key+'|'+str(count)+'\n')
