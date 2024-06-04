# coding=utf-8
'''
Created on May 5, 2016

@author: jivan
'''
from __future__ import print_function

import cPickle
import os
import re
import sys
import urllib2

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
CACHE_DIR = os.path.join(ROOT_DIR, 'cache')
valid_species_directories = ['dla', 'bola', 'fla', 'fish', 'nhp', 'rt1', 'ovar', 'sla']


def scrape_valid_allele_names(species_directory):
    ''' | *brief*: Scrapes the allele names from all fasta files located in *species_directory*.
        | *returns*: A set of strings representing all of the allele names located in
        |    *species_directory*.
    '''
    url = 'ftp://ftp.ebi.ac.uk/pub/databases/ipd/mhc/{}'.format(species_directory)
    url_filename = url.replace(r':', '_').replace(r'/', r'_')
    if not os.path.exists(os.path.join(CACHE_DIR, url_filename)):
        file_index = urllib2.urlopen(url)
        content = file_index.read()
        file_index.close()
        with open(os.path.join(CACHE_DIR, url_filename), 'w+') as f:
            f.write(content)
    else:
        with open(os.path.join(CACHE_DIR, url_filename)) as f:
            content = f.read()

    file_index = urllib2.urlopen(url)
    content = file_index.read()
    # Example line:
    # -rwxr-xr-x    1 ftp      ftp          3087 Oct 23  2013 Aotr-G_nuc.fasta
    fasta_filenames = re.findall(r'[^\s]*fasta', content)
    allele_names = set()
    for filename in fasta_filenames:
        names = scrape_single_file('{}/{}'.format(url, filename))
        print('.', end='')
        sys.stdout.flush()
        allele_names.update(names)
    print(allele_names)
    with open('{}_allele_names.p'.format(species_directory), 'w+') as pf:
        cPickle.dump(list(allele_names), pf)
    return allele_names

def scrape_single_file(url):
    ''' | *brief*: Scrapes allele names from a single fasta file and returns them as a set
        |    of strings.
    '''
    url_filename = url.replace(r':', '_').replace(r'/', r'_')
    if not os.path.exists(os.path.join(CACHE_DIR, url_filename)):
        url_file = urllib2.urlopen(url)
        content = url_file.read()
        url_file.close()
        with open(os.path.join(CACHE_DIR, url_filename), 'w+') as f:
            f.write(content)
    else:
        with open(os.path.join(CACHE_DIR, url_filename)) as f:
            content = f.read()
        
    fasta_sequence_names = re.findall(r'>.*?\n', content)
    allele_names = set()
    for fasta_sequence_name in fasta_sequence_names:
        # Some fasta sequence names have additional information before the allele name
        # Example entry: '>IPD:MHC01877 Mamu-A3*13:05'
        name1 = re.sub(r'>.*? (.*)\n', r'\1', fasta_sequence_name)
        # For names without additional information, just strip the formatting charcters.
        name2 = re.sub(r'>(.*)\n', r'\1', name1)
        # Some names have additional information after the allele name, separated by a space.
        name3 = re.sub(r'(.*?) .*', r'\1', name2)
        # Some names have synonymous DNA substitution and non-coding variant identifiers
        #    (Numbers after the second colon).  Remove these.
        name4 = re.sub(r'(.*?:.*?):.*', r'\1', name3)
        # Some names (particularly SLA sequences) have synonymous DNA substitution and
        #    non-coding variant identifiers but with no colons.  Remove these.
        name5 = re.sub(r'(.*?\*)(\d{4}).*', r'\1\2', name4)
        # Some of the files have an underscore in place of an asterisk
        name6 = name5.replace(r'_', r'*')
        # Some names have left out the colon, add it back in.
        name7 = re.sub(r'(.*?\*)(.\d{1,2})(\d{2}).*', r'\1\2:\3', name6)
        # Some of the files mix alleles and other sequences.  They're easy to spot with a
        #    semicolon remaining after the above formatting
        name = name7
        if ';' not in name:
            allele_names.add(name)

    return allele_names

if __name__ == '__main__':
    if not os.path.exists(CACHE_DIR):
        os.mkdir(CACHE_DIR)

    # If no species directories specified, scrape from all.
    if len(sys.argv) == 1:
        species_directories = valid_species_directories
    else:
        species_directories = []
        for d in sys.argv[1:]:
            if d not in valid_species_directories:
                raise Exception('Unexpected allele directory: {}'.format(d))
            else:
                species_directories.append(d)

    all_allele_names = []
    for species_directory in species_directories:
        print('Getting allele names from "{}" directory'.format(species_directory))
        allele_names = scrape_valid_allele_names(species_directory)
        all_allele_names.extend(allele_names)
    print('{} Non-Human Allele Names Scraped'.format(len(all_allele_names)))
