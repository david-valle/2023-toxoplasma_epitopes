# 2023-toxoplasma_epitopes
Code for finding toxoplasma epitopes common to human brain proteins

### Description

This code can search for potentially immunogenic peptides on T. gondii (or any other organisim if the proper files are provided by the user) and then it matches them with human membrane or extracellular proteins expressed in brain. It then performs a random sampling of non-brain proteins to asess the reliabality of its findings and then analyzes the expression patter of such matches in data derived from developing mice. 

If you have questions, problems or suggestions, contact David Valle-Garcia (see contact info below)

---

### Features
  **-v 0.0.2**

* Replicates the whole analysis
* Performs random sampling (note that, as this is random, the results may be slightly different each time you run it).

### TO-DO(s) in future iterations  
* Change all scripts to Python

---

## Requirements
#### Compatible OS*:
* [Ubuntu 20.04.5 LTS](https://releases.ubuntu.com/focal/)
* MacOS 14.3

#### Incompatible OS*:
* UNKNOWN  

\* The script should run in other UNIX based OS and versions, but testing is required.  

#### Command line Software required:
| Requirement | Version  | Required Commands * |
| :---:   | :---: | :---: |
| [Anaconda](https://www.anaconda.com/download) | 2.6.0 | conda |

Note: Anaconda is the only package that needs to be installed. Other conda environments such as miniconda should also work but are untested. See environment setup for more info

These programs are needed if you wish to use your own environment (not needed if you will use Anaconda):
| Requirement | Version  | Required Commands * |
| :---:   | :---: | :---: |
| [Perl](https://www.perl.org/) | 5.3.30 | perl |
| [Python](https://www.python.org/) | 3.12.13 | python |
| [R](https://www.r-project.org/) | 4.3.3 | Rscript |
| [Linear B cell epitope predictor](http://tools.iedb.org/bcell/download/) | 3.0 | predict_antibody_epitope.py |
| [blastp](https://blast.ncbi.nlm.nih.gov/doc/blast-help/downloadblastdata.html) | 2.6.0 | blastp |

#### Python packages required (included in conda environment you dont need to install them):

```
bedtools version: 2.30.0
```
```
blast version: 2.15.0
```


---

### Installation
Download pipeline from Github repository:  
```
git clone https://github.com/david-valle/2023-toxoplasma_epitopes
```
```
cd 2023-toxoplasma_epitopes
```

---

### Environment set up
Run: 
```
conda env create -f ./env/epitopes_conda.yml
```
```
conda activate epitopes
```

---

### Test our pipeline

* Estimated test time:  **1 minute or less**  

```
./replicate-analysis.sh test
```
Note that test data does not give any matching epitope but the pipeline should run very fast. 

---

## Replicate our analysis:

* Estimated test time:  **20 minute(s)**  

1. To execute our pipeline, run:  
```
./replicate-analysis.sh run
```

2. Your console should print some messages while the analyses are being performed. At the end it should print:  
```
======
 ALL DONE!
======
```

3. Pipeline results for test data should be in the following directory:  
```
./results/
```

---

### Pipeline Results

Inside the directory results/ you can find the following:

* `merged-epitopes.bed  |  bed file` A file with the epitopes coordinates from T. gondii.  

* `sequence-epitopes.fasta  |  fasta file` A file containing epitopes sequences.  

* `human-proteins-cell_surface-BrainS.fasta  |  fasta file` A file containing BrainS sequences.  

* `ids-proteins-cell_surface-BrainS.txt  |  txt file` A file containing the ids of BrainS sequences.   

* `human-proteins-cell_surface-NO_BrainS.fasta  |  fasta file` A file containing NO BrainS sequences. 

* `ids-proteins-cell_surface-NO_BrainS.txt  |  txt file` A file containing the ids of BrainS sequences. 

* `blast-epitopes-BrainS-filtered.txt  |  txt file` A file containing the blast table with matches between epitopes and BrainS sequences.

* `blast-epitopes-BrainS-protein_id-gene_name.txt  |  txt file` A file containing the protein ids and gene names of BrainS proteins that match with epitopes.

* `blast-epitopes-BrainS-gene_name.txt  |  txt file` A file containing the gene names of BrainS proteins that match with epitopes.

* `blast-epitopes-BrainS-protein_id.txt  |  txt file` A file containing the protein ids of BrainS proteins that match with epitopes.

* `Random-NO_BrainS-Matches.txt  |  txt file` A file containing the number of matching sequences from the random sampling of NO BrainS files.  

* `BrainS*  |  blastpdb files` Files containing the blastp database from BrainS proteins.  

---

#### Cite us

If you use our results or pipeline, please, cite us!

https://doi.org/10.3390/biom14080933

Meza-Sosa, K.F.; Valle-Garcia, D.; González-Conchillos, H.; Blanco-Ayala, T.; Salazar, A.; Flores, I.; Gómez-Manzo, S.; González Esquivel, D.F.; Pérez de la Cruz, G.; Pineda, B.; Pérez de la Cruz, V. Molecular Mimicry by Toxoplasma gondii B-Cell Epitopes of Neurodevelopmental Proteins: An Immunoinformatic Approach. Biomolecules 2024, 14, 933. 

---

### Contact
If you have questions, requests, or bugs to report, open an issue in github, or email <david.valle.edu@gmail.com>

#### Dev Team

David Valle-Garcia <david.valle.edu@gmail.com>   

