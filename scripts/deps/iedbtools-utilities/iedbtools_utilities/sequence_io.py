'''
Created on Sep 15, 2015

@author: jivan
'''
import re
valid_amino_acid_chars = 'acdefghiklmnpqrstvwyACDEFGHIKLMNPQRSTVWY'

class FASTASequenceInput(object):
    @staticmethod
    def valid_sequence_text(text):
        ret = True
        if '>' not in text:
            ret = False
        sequences = text.split('>')

        for s_raw in sequences:
            s = s_raw.strip()
            if len(s) == 0: continue

            end_of_name = s.find('\n')
            seq_blocks = s[end_of_name:].split()
            seq = ''.join(seq_blocks)
            seq = seq.upper()
            if not OneSequenceInput.valid_sequence_text(seq):
                ret = False
                break

        return ret

    def __init__(self, fasta_text):
        if '>' not in fasta_text:
            raise ValueError('Expected ">" not found.')
        sequences = fasta_text.split('>')
        text_sequences = []
        sequence_names = []
        for s_raw in sequences:
            s = s_raw.strip()
            if len(s) == 0: continue

            end_of_name = s.find('\n')
            sequence_name = s[:end_of_name].strip()
            sequence_names.append(sequence_name)
            seq_blocks = s[end_of_name:].split()
            seq = ''.join(seq_blocks)
            text_sequences.append(seq.upper())

        self._text_sequences = text_sequences
        self.sequence_names = sequence_names

    def as_amino_acid_text(self):
        return self._text_sequences


class WhitespaceSeparatedSequenceInput(object):
    """ Any whitespace may be used to delineate sequences.
    """
    @staticmethod
    def valid_sequence_text(one_sequence_text):
        regex_str = r'^[{}\s]*$'.format(valid_amino_acid_chars + r' ')
        match = re.match(regex_str, one_sequence_text.strip())
        valid = bool(match)
        return valid

    def __init__(self, one_sequence_text):
        if not self.valid_sequence_text(one_sequence_text):
            msg = 'Invalid space-separated input: {}'.format(one_sequence_text)
            raise ValueError(msg)

        sequences = [s.upper() for s in re.split(r'[\s]', one_sequence_text.strip()) if s != '']
        self.sequence_names = ['ws-separated-{}'.format(i) for i in range(len(sequences))]
        self.text_sequences = sequences

    def as_amino_acid_text(self):
        return self.text_sequences

class OneSequenceInput(object):
    """ All whitespace is ignored, joining all blocks together to form a single sequence.
    """
    @staticmethod
    def valid_sequence_text(one_sequence_text):
        regex_str = r'^[{}\s]*$'.format(valid_amino_acid_chars)
        match = re.match(regex_str, one_sequence_text.strip(), flags=re.MULTILINE)
        valid = bool(match)
        return valid

    def __init__(self, one_sequence_text):
        if not self.valid_sequence_text(one_sequence_text):
            msg = 'Invalid one-sequence input: {}'.format(one_sequence_text)
            raise ValueError(msg)

        # Strip all whitespace from the input.
        sequence = re.sub(r'[\s]+', '', one_sequence_text)
        self.text_sequences = [sequence.upper()]
        self.sequence_names = ['one-sequence']

    def as_amino_acid_text(self):
        return self.text_sequences

class SequenceOutput(object):
    """ | *brief*: Outputs sequences in various formats.
        | *author*: Jivan
        | *created*: 2015-11-27
    """
    @staticmethod
    def to_fasta(sequence_list):
        seq_fasta_strings = []
        for i, seq in enumerate(sequence_list, start=1):
            seq_fasta = '>seq-{}\n{}\n\n'.format(i, seq.upper())
            seq_fasta_strings.append(seq_fasta)
        fasta = ''.join(seq_fasta_strings)
        return fasta

    @staticmethod
    def to_whitespace_separated(sequence_list):
        seq_ws_separated_strings = []
        for i, seq in enumerate(sequence_list, start=1):
            seq_ws_separated = '{}\n\n'.format(seq.upper())
            seq_ws_separated_strings.append(seq_ws_separated)
        whitespace_separated = ''.join(seq_ws_separated_strings)
        return whitespace_separated
