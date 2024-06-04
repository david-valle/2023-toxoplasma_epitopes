2016-05-05 Jivan Amara

Currently contains classes for converting from input formats to a python list of sequences.
    TextSequenceInput
    FASTASequenceInput

These are used like:
    if FASTASequenceInput.valid_sequence_text(filecontent_or_textinput):
        sequence_input = FASTASequenceInput(filecontent_or_textinput)
        sequences = sequence_input.as_amino_acid_text
    else:
        raise('Input is not valid FASTA')

--------------
Also contains a package 'valid_allele_names' with scripts to scrape canonical allele names
and provide them as a simple list of strings.

Used like:

    from valid_allele_names import allele_name_list
    if my_allele_name not in allele_name_list:
        print('Unrecognized allele name: {}'.format(my_allele_name))

To recreate list if sources are updated, run:
 - scrape_valid_human_allele_names.py
 - scrape_valid_non_human_allele_names.py
Files:
 - non_human_allele_names.p
 - human_allele_names.p
should be different.
