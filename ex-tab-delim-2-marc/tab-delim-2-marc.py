#!/usr/bin/python

import pymarc
from pymarc import Record, Field
import datetime

# INPUT FILE(S)
tab_delim_file = open('katrina-tab-data-mod.txt', 'r')
tab_delim_recs = tab_delim_file.readlines()
tab_delim_file.close()

# OUTPUT FILE(S)
marc_recs_out = open('katrina.mrc', 'w')

# List of column headers from the first row of tab-delimited data and their corresponding MARC field tag
#	Index	Column Header:				Assigned to MARC Field:
#	0		Title						245
#	1		Alternate Title				246
#	2		Description (i.e., notes)	500 - should map to various 5XXs
#	3		Url							856
#	4		URL target					as in a page anchor? - add "#" and target to end of URL
#	5		Relation					490/830 - series?
#	6		Rights						506
#	7		Date Issued					260 $c and 008 bytes (Date1)
#	8		Publisher					260 $b
#	9		Creator						100 or 110 - hard to determine with script if personal name or corporate body
#	10		Contributor					700 or 710 - hard to determine with script if personal name or corporate body
#	11		Subject						653 - uncontrolled
#	12		Resource Type				LDR byte 6
#	13		Language					008 byte (Lang)
#	14		Format						not sure what MARC field this might map to
#	15		Table of Contents			505
#	16		Abstract					520
#	17		Genre or Form				655

rec_cnt = 0
for record in tab_delim_recs:
	fields = record.split('\t')		# split the line on tab characters to retrieve a list of field data
	if rec_cnt == 0:
		# Print the list of column headers from the first row of tab-delimited data
		print 'Field List\n----------'
		field_cnt = 0
		for field in fields:
			print 'Field '+str(field_cnt)+': '+field
			field_cnt += 1
	else:
		new_marc_rec = Record()		# generate a new MARC record object
		print '---------------------------------------\nRecord '+str(rec_cnt)
		print 'Before:'
		print new_marc_rec		# NOTE: the only field present in a new Record object is a default LDR field
		
		#--------------------------------------------
		# Modify the default LDR field in the new MARC record object
		rec_LDR = list(new_marc_rec.leader)			# split the LDR bytes into a list so you can modify based on index position
		rec_LDR[5] = 'n'			# code for new record
		res_type = fields[12].strip()
		if res_type == '':
			rec_LDR[6] = 'a'		# code for text
		else:
			rec_LDR[6] = res_type	# if the "Resource Type" is not blank, use that code instead of 'a'
		rec_LDR[7] = 'm'			# code for monographic record
		new_marc_rec.leader = ''.join(rec_LDR)		# join the list of LDR bytes into a string and assign to the 'leader' field of the MARC record
		#--------------------------------------------
		# Create 001 and 040 MARC fields for record number and cataloging source
		rec_001 = Field(tag='001', data='000'+str(rec_cnt))
		rec_040 = Field(tag='040', indicators=[' ',' '], subfields=['a','NNU','b','eng','c','NNU'])
		new_marc_rec.add_ordered_field(rec_001)
		new_marc_rec.add_ordered_field(rec_040)
		#--------------------------------------------
		# Create a 245 Title MARC field
		title = fields[0].strip()
		if not title=='':
			rec_245a = title.split(':')[0]
			rec_245b = title.split(':')[1]
			rec_245 = Field(tag='245', indicators=['0','0'], subfields=['a',rec_245a+':', 'b',rec_245b])
			new_marc_rec.add_ordered_field(rec_245)
		#--------------------------------------------
		# Create a 246 Alternate Title MARC field
		alt_title = fields[1].strip()
		if not alt_title=='':
			rec_246_subs = alt_title.split(':')
			rec_246a = rec_246_subs[0]
			if len(rec_246_subs) > 1:
				rec_246b = rec_246_subs[1]
				rec_246 = Field(tag='246', indicators=['3','0'], subfields=['a',rec_246a+':', 'b',rec_246b])
			else:
				rec_246 = Field(tag='246', indicators=['3','0'], subfields=['a',rec_246a])
			new_marc_rec.add_ordered_field(rec_246)
		#--------------------------------------------
		# Create 5XX fields for "Description" column data
		note = fields[2].strip()
		if not note=='':
			if 'bibliographical' in note or 'references' in note:
				rec_504 = Field(tag='504', indicators=[' ',' '], subfields=['a',note])
				new_marc_rec.add_ordered_field(rec_504)
			elif 'thesis' in note or 'Thesis' in note:
				rec_502 = Field(tag='502', indicators=[' ',' '], subfields=['a',note])
				new_marc_rec.add_ordered_field(rec_502)
			else:
				rec_500 = Field(tag='500', indicators=[' ',' '], subfields=['a',note])
				new_marc_rec.add_ordered_field(rec_500)
		#--------------------------------------------
		# Create 856 field for URL + URL target
		url = fields[3].strip()
		url_tgt = fields[4].strip()
		if not url=='':
			if not url_tgt=='':
				url = url+'#'+url_tgt		# add the "page anchor" to the end of the URL
			rec_856 = Field(tag='856', indicators=['4','0'], subfields=['u',url])
			new_marc_rec.add_ordered_field(rec_856)
		#--------------------------------------------
		# Create 490 field for "Relation" (i.e., Series title) - could also create authorized 830 field if you want to trace the series
		series = fields[5].strip()
		if not series=='':
			rec_490 = Field(tag='490', indicators=['0',' '], subfields=['a',series])
			new_marc_rec.add_ordered_field(rec_490)
		#--------------------------------------------
		# Create 506 field for the Rights statement
		rights = fields[6].strip()
		if not rights=='':
			rec_506 = Field(tag='506', indicators=[' ',' '], subfields=['a',rights])
			new_marc_rec.add_ordered_field(rec_506)
		#--------------------------------------------
		# Create 260 field for the Publisher and Date Issued fields
		date = fields[7].strip()
		pub = fields[8].strip()
		rec_260 = Field(tag='260', indicators=[' ',' '])
		add_260 = False
		if not pub=='':
			rec_260.add_subfield('b',pub)
			add_260 = True
		if not date=='':
			rec_260.add_subfield('c',date)
			add_260 = True
		if add_260:
			new_marc_rec.add_ordered_field(rec_260)
		#--------------------------------------------
		# Create 008 field with Date Issued as bytes 07-10 (Date1) and Language as bytes 35-37
		# Descriptions of the 008 fields are at: http://www.oclc.org/bibformats/en/fixedfield.html
		# For breakdown of 008 byte positions, see: http://www.oclc.org/bibformats/en/fixedfield/008summary.html
		curr_date = datetime.date.today()
		yy = str(curr_date.year)[2:].zfill(2)
		mm = str(curr_date.month).zfill(2)
		dd = str(curr_date.day).zfill(2)
		entered = yy+mm+dd
		dtst = 's'
		if not date=='':
			date1 = date				# NOTE: this only works if the content of the Date column in the original data is in the format YYYY
		else:
			date1 = 'uuuu'				# enter date1 as unknown if no date is specified in the data
		date2 = '    '
		ctry = 'xxu'					# use the default code for "United States" as the country of publication
		illus = '    '					# enter blanks for illustration codes - can enter 'a   ' if you think the materials would be illustrated
		audn = ' '						# audience not specified
		form = ' '						# form not specified - can enter 's' (electronic), 'o' (online), or 'q' (direct electronic) if known as e-resources
		if 'bibliographical' in note or 'references' in note:
			cont = 'b   '				# item contains bibliographical references
		else:
			cont = '    '				# nature of contents is not specified
		gpub = ' '						# use code [blank] to indicate item is not a government publication
		conf = '0'						# use code '0' to indicate item is not a conference publication
		fest = ' '						# use code '0' to indicate item is not a festschrift
		index = '0'						# use code '0' to indicate item does *not* have an index (or use maybe code as '1' if the term "index" is present in the note field)
		pos_32 = ' '					# byte 32 is undefined for books
		litF = '0'						# use code '0' to indicate item is *not* fiction
		biog = ' '						# use code [blank] to indicate item does *not* contain biographical material
		lang_code = fields[13].strip()	# this data must be formatted as the 3-char language codes
		if lang_code=='':
			lng = 'eng'					# use English (eng) as the default language code if a language is not specified in the data
		else:
			lng = lang_code
		mrec = ' '						# use code [blank] for Modified Record to indicate this is an original record
		cat_src = 'd'					# use code 'd' for Cataloging Source to indicate the cataloging organization is not LC or Coop-Cat member
		
		rec_008 = Field(tag='008', data = entered + dtst + date1 + date2 + ctry + illus + audn + form + cont + gpub + conf + fest + index + pos_32 + litF + biog + lng + mrec + cat_src)
		new_marc_rec.add_ordered_field(rec_008)
		
		#--------------------------------------------
		# Create 100 field for the Creator - not able to distinguish if personal name or corporate body, so would mark field as "$2local"
		creator = fields[9].strip()
		if not creator=='':
			rec_100 = Field(tag='100', indicators=['1',' '], subfields=['a',creator,'2','local'])
			new_marc_rec.add_ordered_field(rec_100)
		#--------------------------------------------
		# Create 700 field for the Contributor - not able to distinguish if personal name or corporate body, so would mark field as "$2local"
		contributor = fields[10].strip()
		if not contributor=='':
			rec_700 = Field(tag='700', indicators=['1',' '], subfields=['a',contributor,'2','local'])
			new_marc_rec.add_ordered_field(rec_700)
		#--------------------------------------------
		# Create 653 field for the Subject terms (using uncontrolled subject field)
		subjects = fields[11].strip()
		if not subjects=='':
			rec_653 = Field(tag='653', indicators=[' ',' '], subfields=['a',subjects])
			new_marc_rec.add_ordered_field(rec_653)
		#--------------------------------------------
		# Create 505 field for the Table of Contents
		toc = fields[15].strip()
		if not toc=='':
			rec_505 = Field(tag='505', indicators=['0',' '], subfields=['a',toc])
			new_marc_rec.add_ordered_field(rec_505)
		#--------------------------------------------
		# Create 520 field for the Abstract
		abstract = fields[16].strip()
		if not abstract=='':
			rec_520 = Field(tag='520', indicators=['3',' '], subfields=['a',abstract])
			new_marc_rec.add_ordered_field(rec_520)
		#--------------------------------------------
		# Create 655 field for the Genre/Form term
		# NOTE: if multiple terms are used in the field, you may want to try to break them up if they're separated by commas or other consistent punctuation
		# Marked field as $2local since it may not be authorized term
		genre = fields[17].strip()
		if not genre=='':
			rec_655 = Field(tag='655', indicators=[' ','7'], subfields=['a',genre,'2','local'])
			new_marc_rec.add_ordered_field(rec_655)
		
		
		print 'After:'
		print new_marc_rec
		marc_recs_out.write(new_marc_rec.as_marc())
	
 	rec_cnt += 1

marc_recs_out.close()
