'''
Created on Sep 16, 2015

@author: jivan
'''
from collections import namedtuple
from unittest import TestCase
from sequence_io import FASTASequenceInput, WhitespaceSeparatedSequenceInput, OneSequenceInput
from sequence_io import SequenceOutput

InOutPair = namedtuple('InOutPair', ['input', 'expected_output'])

class CheckFASTASequenceInput(TestCase):
    def test_basic_use(self):
        # test cases
        tcs = [
            InOutPair('>sequence-1\nFNCLGMSNRDFLEGVSGA\n> sequence-2\nCLGMSNRDFLEGVSG',
                      ['FNCLGMSNRDFLEGVSGA', 'CLGMSNRDFLEGVSG']),
            InOutPair('> sequence-1\nFnclGMSNRDFLEGVsga\n> sequence-2\nClgmSNRDFlegVsG',
                      ['FNCLGMSNRDFLEGVSGA', 'CLGMSNRDFLEGVSG']),
        ]
        for fasta_in, expected_sequence_list in tcs:
            self.assertTrue(FASTASequenceInput.valid_sequence_text(fasta_in))
            fsi = FASTASequenceInput(fasta_in)
            expected_sequences = expected_sequence_list
            self.assertEqual(fsi.as_amino_acid_text(), expected_sequences)
            expected_names = ['sequence-1', 'sequence-2']
            self.assertEqual(fsi.sequence_names, expected_names)

    def test_leading_newlines(self):
        # test cases
        tcs = [
            InOutPair('\n\n> sequence-1\nFNCLGMSNRDFLEGVSGA\n> sequence-2\nCLGMSNRDFLEGVSG',
                      ['FNCLGMSNRDFLEGVSGA', 'CLGMSNRDFLEGVSG']),
            InOutPair('\n>sequence-1\nFnclGMSNRDFLEGVsga\n> sequence-2\nClgmSNRDFlegVsG',
                      ['FNCLGMSNRDFLEGVSGA', 'CLGMSNRDFLEGVSG']),
        ]
        for fasta_in, expected_sequence_list in tcs:
            self.assertTrue(FASTASequenceInput.valid_sequence_text(fasta_in))
            fsi = FASTASequenceInput(fasta_in)
            expected_sequences = expected_sequence_list
            self.assertEqual(fsi.as_amino_acid_text(), expected_sequences)
            expected_names = ['sequence-1', 'sequence-2']
            self.assertEqual(fsi.sequence_names, expected_names)

class CheckWhitespaceSeparatedSequenceInput(TestCase):
    def test_basic_use(self):
        # Test Cases
        tcs = [
            InOutPair('FNCLGMSNRDFLEGVSGA CLGMSNRDFLEGVSG LEGDSCVTIMSKD',
                      ['FNCLGMSNRDFLEGVSGA', 'CLGMSNRDFLEGVSG', 'LEGDSCVTIMSKD']),
            InOutPair('FNCLgmsNRDFLEGVSGA clgmSNRDFLEGVSG legdscvtimskd',
                      ['FNCLGMSNRDFLEGVSGA', 'CLGMSNRDFLEGVSG', 'LEGDSCVTIMSKD']),
            InOutPair('FNCLgmsNRDFLEGVSGA\n\nclgmSNRDFLEGVSG\nlegdscvtimskd',
                      ['FNCLGMSNRDFLEGVSGA', 'CLGMSNRDFLEGVSG', 'LEGDSCVTIMSKD']),
        ]
        for tc in tcs:
            self.assertTrue(WhitespaceSeparatedSequenceInput.valid_sequence_text(tc.input))
            wssi = WhitespaceSeparatedSequenceInput(tc.input)
            output = wssi.as_amino_acid_text()
            self.assertEqual(output, tc.expected_output)
            expected_names = ['ws-separated-0', 'ws-separated-1', 'ws-separated-2']
            self.assertEqual(wssi.sequence_names, expected_names)

class CheckOneSequenceInput(TestCase):
    def test_basic_use(self):
        # Test Cases
        tcs = [
            InOutPair('FNCLGMSNRDFLEGVSGA CLGMSNRDFLEGVSG \nLEGDSCVTIMSKD',
                      ['FNCLGMSNRDFLEGVSGACLGMSNRDFLEGVSGLEGDSCVTIMSKD']),
            InOutPair('FNCLgmsNRDFLEGVSGA clgmSNRDFLEGVSG \nlegdscvtimskd',
                      ['FNCLGMSNRDFLEGVSGACLGMSNRDFLEGVSGLEGDSCVTIMSKD']),
        ]
        for one_sequence_input, expected_seq_list in tcs:
            self.assertTrue(OneSequenceInput.valid_sequence_text(one_sequence_input))
            osi = OneSequenceInput(one_sequence_input)
            self.assertEqual(osi.as_amino_acid_text(), expected_seq_list)
            expected_names = ['one-sequence']
            self.assertEqual(osi.sequence_names, expected_names)

class SequenceOutputTests(TestCase):
    def test_to_fasta(self):
        # Test cases
        tcs = [
            InOutPair(['FNCLGMSNRDFLEGVSGA'], '>seq-1\nFNCLGMSNRDFLEGVSGA\n\n'),
            InOutPair(['FNCLGMSNRDFLEGVSGA', 'CLGMSNRDFLEGVSG'],
                      '>seq-1\nFNCLGMSNRDFLEGVSGA\n\n>seq-2\nCLGMSNRDFLEGVSG\n\n'),
            InOutPair(['fnclGMSNRdflEGVSGA'], '>seq-1\nFNCLGMSNRDFLEGVSGA\n\n'),
            InOutPair(['FNClgmsnrdfLEGVSGA', 'clgmsnrdflegvsg'],
                      '>seq-1\nFNCLGMSNRDFLEGVSGA\n\n>seq-2\nCLGMSNRDFLEGVSG\n\n'),
        ]

        for sequence_list, expected_fasta in tcs:
            fasta = SequenceOutput.to_fasta(sequence_list)
            self.assertEqual(fasta, expected_fasta)

    def test_to_whitespace_separated(self):
        # Test cases
        tcs = [
            InOutPair(['FNCLGMSNRDFLEGVSGA'], 'FNCLGMSNRDFLEGVSGA\n\n'),
            InOutPair(['FNCLGMSNRDFLEGVSGA', 'CLGMSNRDFLEGVSG'], 
                      'FNCLGMSNRDFLEGVSGA\n\nCLGMSNRDFLEGVSG\n\n'),
            InOutPair(['fnclgMSNRDFLEGVsga'], 'FNCLGMSNRDFLEGVSGA\n\n'),
            InOutPair(['FNCLGMSNRDFLEGVSGA', 'clgmsnrdflegvsg'],
                      'FNCLGMSNRDFLEGVSGA\n\nCLGMSNRDFLEGVSG\n\n'),
        ]
        
        for sequence_list, expected_whitespace_separated in tcs:
            whitespace_separated = SequenceOutput.to_whitespace_separated(sequence_list)
            self.assertEqual(whitespace_separated, expected_whitespace_separated)
        