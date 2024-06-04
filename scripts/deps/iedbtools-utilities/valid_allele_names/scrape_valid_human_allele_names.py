# coding=utf-8
'''
Created on May 5, 2016

@author: jivan
'''
import cPickle
import itertools
import re

import requests

from web_utilities import HTMLTableStripper


def get_valid_hla_class_i_allele_names():
    resp = requests.request('GET', 'http://hla.alleles.org/alleles/class1.html')
    ts = HTMLTableStripper()
    ts.feed(resp.content)
    table_contents = ts.get_table_contents()
    flat_table_contents = list(itertools.chain.from_iterable(table_contents))

    valid_allele_names = set()
    valid_gene_indicators = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'P', 'V', 'Y']
    table_headers = [ 'HLA-{}'.format(gene_indicator) for gene_indicator in valid_gene_indicators]
    for cell_content in flat_table_contents:
        if cell_content in table_headers: continue

        # Prepend 'HLA-' to allele name
        allele_name_1 = re.sub(r'^(\w)', r'HLA-\1', cell_content)
        # Eliminate content of name from second colon on (not needed to name allele for predictions)
        allele_name = re.sub(r'(.*?:.*?):.*', r'\1', allele_name_1)
        valid_allele_names.add(allele_name)

    return list(valid_allele_names)

def get_valid_hla_class_ii_allele_names():
    resp = requests.request('GET', 'http://hla.alleles.org/alleles/class2.html')
    ts = HTMLTableStripper()
    ts.feed(resp.content)
    table_contents = ts.get_table_contents()
    flat_table_contents = list(itertools.chain.from_iterable(table_contents))

    valid_allele_names = set()
    valid_gene_indicators = [
        'DRA',
        'DRB1', 'DRB2', 'DRB3', 'DRB4', 'DRB5', 'DRB6', 'DRB7', 'DRB8', 'DRB9',
        'DQA1', 'DQB1', 'DPA1', 'DPB1', 'DPB2', 'DMA', 'DMB', 'DOA', 'DOB'
    ]
    table_headers = [ 'HLA-{}'.format(gene_indicator) for gene_indicator in valid_gene_indicators]
    table_headers.append('HLA-DRB2-9')
    for cell_content in flat_table_contents:
        if cell_content in table_headers: continue

        # Prepend 'HLA-' to allele name
        allele_name_1 = re.sub(r'^(\w)', r'HLA-\1', cell_content)
        # Eliminate content of name from second colon on (not needed to name allele for predictions)
        allele_name = re.sub(r'(.*?:.*?):.*', r'\1', allele_name_1)
        valid_allele_names.add(allele_name)

    return list(valid_allele_names)

def get_valid_other_allele_names():
    resp = requests.request('GET', 'http://hla.alleles.org/alleles/classo.html')
    ts = HTMLTableStripper()
    ts.feed(resp.content)
    table_contents = ts.get_table_contents()
    flat_table_contents = list(itertools.chain.from_iterable(table_contents))

    valid_allele_names = []
    valid_gene_indicators = ['HFE', 'MICA', 'MICB', 'TAP1', 'TAP2']
    table_headers = valid_gene_indicators
    for cell_content in flat_table_contents:
        if cell_content in table_headers: continue

        allele_name = cell_content
        valid_allele_names.append(allele_name)

    return valid_allele_names

if __name__ == '__main__':
    names1 = get_valid_hla_class_i_allele_names()
    names2 = get_valid_hla_class_ii_allele_names()
    names3 = get_valid_other_allele_names()
    all_names = names1 + names2 + names3

    print('{} Human Allele Names'.format(len(all_names)))
    with open('human_allele_names.p', 'w+') as pf:
        cPickle.dump(all_names, pf)
