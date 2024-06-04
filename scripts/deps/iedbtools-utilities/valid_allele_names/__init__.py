import cPickle
import os
from pkg_resources import resource_filename
from scrape_valid_non_human_allele_names import valid_species_directories

DIRPATH = os.path.abspath(os.path.dirname(__file__))

human_allele_pickle_file = resource_filename('valid_allele_names', 'human_allele_names.p')

non_human_allele_pickle_filenames = [
    resource_filename('valid_allele_names', '{}_allele_names.p'.format(species_dir))
        for species_dir in valid_species_directories
]

# All of the human allele names are stored in a single pickle file
with open(human_allele_pickle_file) as hpf:
    human_allele_names = cPickle.load(hpf)

allele_name_list = human_allele_names

# Each non-human directory (See scrape_valid_non_human_allele_names.valid_species_directories)
#    gets its own pickle file so scrape updates can be quick if they only target a single
#    directory.
for non_human_allele_pickle_filename in non_human_allele_pickle_filenames:
    with open(non_human_allele_pickle_filename) as nhpf:
        non_human_allele_names = cPickle.load(nhpf)
    allele_name_list.extend(non_human_allele_names)
