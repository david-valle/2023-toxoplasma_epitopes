# 2023-toxoplasma_epitopes
Code for finding toxoplasma epitopes common to human brain proteins

### Description

This code can search for potentially immunogenic peptides on T. gondii (or any other organisim if the proper files are provided by the user) and then it matches them with human membrane or extracellular proteins expressed in brain. It then performs a random sampling of non-brain proteins to asess the reliabality of its findings and then analyzes the expression patter of such matches in data derived from developing mice. 

If you have questions, problems or suggestions, contact David Valle-Garcia (see contact info below)

---

### Features
  **-v 0.0.1**

* Replicates the whole analysis
* Performs random sampling (note that, as this is random, the results may be slightly different each time you run it).

### TO-DO(s) in future iterations  
* Change all scripts to Python
* Make a conda environment for easy deployment and installation

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
|:---------:|:--------:|:-------------------:|
| [Perl](https://www.perl.org/) | 5.3.30 | perl |
| [R](https://www.r-project.org/) | 4.3.3 | Rscript |
| [Python](https://www.python.org/) | 3.12.13 | python |
| [Linear B cell epitope predictor](http://tools.iedb.org/bcell/download/) | 3.0 | predict_antibody_epitope.py |
| [blastp](https://blast.ncbi.nlm.nih.gov/doc/blast-help/downloadblastdata.html) | 2.6.0 | blastp |
| [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) | 24.1.2 | conda |

\* These commands must be accessible from your `$PATH` (*i.e.* you should be able to invoke them from your command line).  
Note: conda is not needed but advised to install all python packages and dependencies.


#### Python packages required:

```
bedtools version: 2.30.0
```

#### R packages required:

```
cowplot version: 1.1.1
```

---

### Installation
Download pipeline from Github repository:  
```
git@github.com:david-valle/2023-toxoplasma_epitopes.git
```

---

## Replicate our analysis:

* Estimated test time:  **20 minute(s)**  

1. To execute our pipeline, run:  
```
./replicate-analysis.sh
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

* A `.merged-all_methods.bed bed file` A file with the epitopes coordinates from T. gondii.  

* A `.sequence-all_methods.fasta fasta file` A file containing epitopes sequences.   

---

#### Cite us

TO-DO: add reference to our paper once published

---

### Contact
If you have questions, requests, or bugs to report, open an issue in github, or email <david.valle.edu@gmail.com>

#### Dev Team
David Valle-Garcia <david.valle.edu@gmail.com>   

