import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(
    name="iedbtools-utilities",
    version="0.11.1",
    packages=['iedbtools_utilities', 'valid_allele_names', 'web_utilities'],
    description='IEDB Tools Utilties regularly used across projects.',
    long_description=README,
    package_data={
        'valid_allele_names': [
            'human_allele_names.p', 'dla_allele_names.p', 'bola_allele_names.p',
            'fla_allele_names.p', 'fish_allele_names.p', 'nhp_allele_names.p',
            'rt1_allele_names.p', 'ovar_allele_names.p', 'sla_allele_names.p'
        ]
    },
    # Important only if the package will be widely distributed.  See more at:
    #    https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
    ]
)
