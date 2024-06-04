'''
Created on Apr 20, 2016

@author: jivan
'''

def split_sequence(sequence, subsequence_length):
    '''
        Returns a list containing subsequences of length *subsequence_length*.
    '''
    peptide_list = []
    num = len(sequence.strip()) - subsequence_length + 1
    for i in range(num):
        peptide = sequence[i:i + subsequence_length]
        peptide_list.append(peptide)
    return peptide_list
