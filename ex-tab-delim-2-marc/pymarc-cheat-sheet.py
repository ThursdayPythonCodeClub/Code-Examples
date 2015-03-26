# Common PyMARC functions
# Documentation at:  https://github.com/edsu/pymarc

# pymarc.MARCReader(file('filename.mrc'), to_unicode=True, force_utf8=True
# pymarc.MARCWriter(file('filename.mrc', 'w')
# record.add_field()
# record.add_ordered_field()
# record.get_fields()
# record.remove_field()
# field.add_subfield()
# field.get_subfields()
# field.delete_subfield()

#####################################################
# READ input from or WRITE output to .mrc MARC files
# Read in an .mrc input file of MARC records and assign to a variable:
  marc_recs_in = pymarc.MARCReader(file('my_marc_input.mrc'), to_unicode=True, force_utf8=True)
  
# Create an .mrc file object to write out MARC records to the file
  marc_recs_out = pymarc.MARCWriter(file('my_marc_output.mrc', 'w'))

#####################################################
# Record-level functions:  https://github.com/edsu/pymarc/blob/master/pymarc/record.py
# ADD FIELD to record
  record.add_field(my_field_obj)          # add a new field object to the end of the MARC record
  record.add_ordered_field(my_field_obj)  # add a new field object to the MARC record in field tag order
# GET FIELDS from a record
  record.get_fields('100','110','245')    # returns a list of all the fields for the specified tags
        # example of how to get a list of all the subject fields
            subjects = record.get_fields('600','610','650','651')
        # you can then iterate through each of the subject fields using:
            for my_subject in subjects:
              if my_subject.indicator2 == '0':
                lcsh = True
              else:
                lcsh = False
  record.get_fields()                     # returns *all* the fields in the record
# DELETE FIELD from a record
  record.remove_field(my_field_obj)       # delete a field object from the MARC record
        # example of how to delete all the 035 fields from a record
            for my_rec_035 in record.get_fields('035'):
              record.remove_field(my_rec_035)
#####################################################
# Field-level functions:  https://github.com/edsu/pymarc/blob/master/pymarc/field.py
# ADD SUBFIELD to field
    field.add_subfield(my_subfield_code, my_subfield_content)
        # example to add a subfield $h for the GMD to the 245 field
          my_field_245.add_subfield('a','[electronic resource]')
# GET SUBFIELDS from a field
    field.get_subfields('a', 'b')       # returns a list of all the subfields for the specified codes
        # example to get and create a list of all the ISBNs from 020 fields
          rec_020s = record.get_fields('020')
          for rec_020 in rec_020s:
            valid_ISBNs = rec_020.get_subfields('a')
            invalid_ISBNs = rec_020.get_subfields('z')
# DELETE SUBFIELD from a field
    field.delete_subfield('a')          # delete ONLY the first subfield with the specified code and returns it's value
        # example to remove any relator subfields from 700 fields
          rec_700s = record.get_fields('700')         # retrieve a list of all the 700 fields
          for rec_700 in rec_700s:                    # iterate through the list of 700 fields
            for sub_e in rec_700.get_subfields('e'):  # iterate through a list of all the subfield $e's found in the 700 field
              rec_700.delete_subfield('e')            # delete the subfield $e from the 700 field


