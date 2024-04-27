# 2023-toxoplasma_epitopes
Code for finding toxoplasma epitopes common to human brain proteins

# needs to be updated! the infi bellow is just an example

### Workflow overview
TO-DO: Include code flow

===  

- TO-DO: Descrition at large

- This pipeline is meant to reproduce the results in: TO-DO-add url and doi after paper is published

The pipeline takes as INPUT an excel samplesheet created by UGPM, LaNSE, Cinvestav-IPN from a Synapt G2-Si Mass Spectrometer. Contact Emmanuel Castro-Rios (eriosc@cinvestav.mx) for more info. It also takes a .csv samplesheet describing sampleID_replicate and the condition (i.e. control vs treatment). 

'Proteomic compare' is a pipeline tool that takes peptide quantifications in excel format and process it to generate a volcano plot and PCA of comparisons between conditions. This pipeline generates the followin outputs:  
For each INPUT .xlsx
1) a figurte of a volcano plot with UP and DOWN peptides;  
2) a figure same as 1) but with labeled peptides;  
3) a figure of a PCA plot created from the UP and DOWN peptides;
4) a figure of a panel diagnostics for 3), including a screeplot, a Parallel Coordinate Plot, a Biplot, and a labeled PCA with sample names.  

---

### Features
  **-v 0.0.1**

* Supports .xlsx files from  UGPM, LaNSE, Cinvestav-IPN from a Synapt G2-Si Mass Spectrometer
* Results include labelled and unlabelled volcano plot
* Results include PCA and a diagnostics screeplot, PCP, and biplot
* Scalability and reproducibility via a Nextflow-based framework

### TO-DO(s)  
* Easy deploy with docker
* Make docker outputs not root owned

---

## Requirements
#### Compatible OS*:
* [Ubuntu 20.04.5 LTS](https://releases.ubuntu.com/focal/)

#### Incompatible OS*:
* UNKNOWN  

\* Proteomic compare may run in other UNIX based OS and versions, but testing is required.  

#### Command line Software required:
| Requirement | Version  | Required Commands * |
|:---------:|:--------:|:-------------------:|
| [Nextflow](https://www.nextflow.io/docs/latest/getstarted.html) | 22.10.4 | nextflow |
| [R](https://www.r-project.org/) | 4.2.2 | Rscript |

\* These commands must be accessible from your `$PATH` (*i.e.* you should be able to invoke them from your command line).  

#### R packages required:

```
cowplot version: 1.1.1
dplyr version: 1.1.2
factoextra version: 1.0.7
ggplot2 version: 3.4.2
ggrepel version: 0.9.3
ggsci version: 3.0.0
matrixStats version: 1.0.0
openxlsx version: 4.2.5.2
scales version: 1.2.1
stringr version: 1.5.0
tidyr version: 1.3.0
```

---

### Installation
Download pipeline from Github repository:  
```
git@github.com:Iaguilaror/low_BMD_in_PMWMX.git
```

---

## Replicate our analysis (Testing the pipeline):

* Estimated test time:  **5 minute(s)**  

1. To test pipeline execution using test data, run:  
```
./runtest.sh
```

2. Your console should print the Nextflow log for the run, once every process has been submitted, the following message will appear:  
```
======
 Basic pipeline TEST SUCCESSFUL
======
```

3. Pipeline results for test data should be in the following directory:  
```
./paper-results/
```


---

### Usage
TO-DO

### Pipeline Inputs

* An `.xlsx excel samplesheet` created by UGPM, LaNSE, Cinvestav-IPN from a Synapt G2-Si Mass Spectrometer. Contact Emmanuel Castro-Rios (eriosc@cinvestav.mx) for more info.  

NAMING CONVENTION: filename should be CONDITION1_vs_CONDITION2.xlsx, because the condition names will be taken from the filename.  

Example contents  
```
sheet number or name: 1
Accession	Peptide count	Unique peptides	Confidence score	Anova (p)	nlog.Anova	q Value	Max fold change	Power	Highest mean condition	Lowest mean condition	Mass	Description	20220608_34_HDMSE_N_P1_R001	20220608_34_HDMSE_N_P1_R002	20220608_34_HDMSE_N_P1_R003	20220608_35_HDMSE_N_P2_R001
Q2M243;J3QKX2	5	1	27.3012	3.90E-08	7.40898498193687	3.45E-07	4.42850961640127	0.999999916484847	Normal	Osteoporosis	75867.8723	Coiled-coil domain-containing protein 27 OS=Homo sapiens OX=9606 GN=CCDC27 PE=1 SV=2	37894.2229766787	44809.8331347101	37940.595720904	61166.4163882289
...
```

* A `.csv samplesheet` describing sampleID_replicate and the condition.  
Example lines  
```
muestra	condition
20220608_34_HDMSE_N_P1_R001	Normal
20220608_34_HDMSE_N_P1_R002	Normal
20220608_34_HDMSE_N_P1_R003	Normal
20220608_44_HDMSE_OP_PI_R001	OP
20220608_44_HDMSE_OP_PI_R002	OP
20220608_44_HDMSE_OP_PI_R003	OP
...
```
---

### Pipeline Results

Inside the directory paper-results/ you can find the following:

* A `.volcano.png figure` with the figure showing a volcano plot.  

* A `.volcano.named.png image` same as above but highlighting top UP and DOWN peptides.  

* A `.UP_and_DOWN_hits.xlsx excel file` that includes only UP and DOWN differentiated peptides according to the thresholds hardcoded in the volcano.R script.  

* A `.PCA_main.png figure` with the figure showing a PCA for two conditions.  

* A `PCA_diagnostic.png image` same as above but showing a panel with: screeplot, labeled PCA, a Parallel Coordinate Plot, and a biplot. Meant to provide an overview of the whole PCA.  

---
#### References
Under the hood Proteomic compare uses some coding tools, please include the following ciations in your work:

* Di Tommaso, P., Chatzou, M., Floden, E. W., Barja, P. P., Palumbo, E., & Notredame, C. (2017). Nextflow enables reproducible computational workflows. Nature Biotechnology, 35(4), 316–319. doi:10.1038/nbt.3820

* Team, R. C. (2017). R: a language and environment for statistical computing. R Foundation for Statistical Computing, Vienna. http s. www. R-proje ct. org.

TO-DO: explore citations and ackowledgments for used R packages.

---

### Contact
If you have questions, requests, or bugs to report, open an issue in github, or email <david.valle.edu@gmail.com>

#### Dev Team
David Valle-Garcia <david.valle.edu@gmail.com>   

### Cite us
 TO-DO
