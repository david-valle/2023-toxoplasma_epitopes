#!/bin/bash

# By running this script you can fully replicate the results from our paper
# See Readme.md for more info


# ------
# Step 0 -- Set environment variables
# ------

## 0.1 Folders

I=intermediates 	### Here you will save the intermediate files. Modify if needed
R=results 			### Here you will save the final results. Modify if needed
S=scripts 			### This folder contains the scripts needed to run the analysis
D=data 				### This folder contains the Input data

## 0.2 Create intermediates and results directories if they don't exist

mkdir -p $I
mkdir -p $R

## 0.3 Files 

FASTA_TOXO="$D/T_gondii_RH88-proteins.fasta"  

if [ $1 == "test" ] # Change dataset if the test mode is on
then
	FASTA_TOXO="$D/test.fasta"
fi

FASTA_HUMAN="$D/human-proteins-cell_surface.fasta"

## 0.4 Methods

METHODS="Chou-Fasman Emini Karplus-Schulz Kolaskar-Tongaonkar Parker" ### You can edit this list to modify the methods used for peptide prediction


## 0.4 Filters

N=3 ### Number of threads used for the alignment. Modify if necessary.

SCORE=1 ### Score filter for immunogenic peptides prediction
COVERAGE=80  ### Coverage filter for blastp alignments
EVALUE=0.1  ### Evalue filter for immunogenic peptides prediction
RANDOMN=100  ### Number of random samplings (see step 3)



# ------
# Step 1 -- Predict, filter and merge epitopes
# ------

echo "------"
echo "Step 1 -- Predict, filter and merge epitopes"
echo "------"


## 1.1 Predict epitopes with all 5 algorithms

for M in $METHODS
do
     python $S/predict_antibody_epitope.py -m $M -f $FASTA_TOXO > $I/out-$M.txt
done

echo "Total predicted peptides per method"
wc -l $I/out-*.txt

## 1.2 FIlter the results with a score greater or equal than $SCORE (1 by default) and write a bed file

for M in $METHODS
do
	$S/filter_peptides.pl $I/out-${M}.txt $SCORE > $I/filtered-$M.bed
done

echo "Total filtered predicted peptides per method"
wc -l $I/filtered-*.bed

## 1.3 Merge overlapping peptides per method

for M in $METHODS
do
	sortBed -i $I/filtered-$M.bed | mergeBed -c 4 -o mean -i - > $I/merged-$M.bed
done

echo "Total merged peptides per method"
wc -l $I/merged-*.bed

## 1.4 Calculate average size per method

for M in $METHODS
do
	echo "Average peptide size for $M"
	awk 'BEGIN{n=0; t=0} { s=$3-$2; t=t+s; n++;} END {prom=t/n; print prom}' $I/merged-$M.bed
done

## 1.5 Merge overlapping peptides between methods

cat $I/merged-*.bed | sortBed -i - | mergeBed -c 4 -o mean -i - > $R/merged-epitopes.bed

echo "Total merged peptides between all methods"
wc -l $R/merged-epitopes.bed

## 1.6 Calculate average size for all methods

echo "Average peptide size for all methods"
awk 'BEGIN{n=0; t=0} { s=$3-$2; t=t+s; n++;} END {prom=t/n; print prom}' $R/merged-epitopes.bed

## 1.6 Get sequences for merged epitopes

fastaFromBed -fi $FASTA_TOXO -fo $I/sequence-epitopes.tab -bed $R/merged-epitopes.bed -tab

## 1.7 Merge duplicated sequences

cut -f2 $I/sequence-epitopes.tab | sort | uniq -d > $I/temp
$S/filter_dup.pl $I/sequence-epitopes.tab $I/temp > $R/sequence-epitopes.fasta
rm $I/temp
echo "Total non-redundant peptide sequences"
grep ">" $R/sequence-epitopes.fasta | wc -l


# ------
# Step 2 -- Align epitopes to brain surface proteins
# ------

echo ""
echo "------"
echo "Step 2 -- Align epitopes to brain surface proteins"
echo "------"

## 2.1 Create lists of BrainS (Brain surface) and NO BrainS proteins

for CELL in neuron astrocyte oligodendrocyte microglia
do
	cat $D/ids-proteins-${CELL}_differentiation.txt $D/ids-proteins-cell_surface.txt | sort | uniq -d > $I/ids-proteins-${CELL}_differentiation-cell_surface.txt
done

cat $I/ids-proteins-*_differentiation-cell_surface.txt | sort | uniq > $R/ids-proteins-cell_surface-BrainS.txt
cat $R/ids-proteins-cell_surface-BrainS.txt $D/ids-proteins-cell_surface.txt | sort | uniq -u > $R/ids-proteins-cell_surface-NO_BrainS.txt

BRAINSN=$(wc -l $R/ids-proteins-cell_surface-BrainS.txt | awk '{print $1}')  ### Number of BrainS proteins, used for random sampling. 372
NOBRAINSN=$(wc -l $R/ids-proteins-cell_surface-NO_BrainS.txt | awk '{print $1}')   ### Number of NO BrainS proteins, used for random sampling. 2251


## 2.2 Create fasta of BrainS (Brain surface) and NO BrainS proteins

$S/filter_fasta.pl $FASTA_HUMAN $R/ids-proteins-cell_surface-BrainS.txt > $R/human-proteins-cell_surface-BrainS.fasta
$S/filter_fasta.pl $FASTA_HUMAN $R/ids-proteins-cell_surface-NO_BrainS.txt -e > $R/human-proteins-cell_surface-NO_BrainS.fasta

## 2.3 Create blastp database

makeblastdb -dbtype prot -in $R/human-proteins-cell_surface-BrainS.fasta -title BrainS -parse_seqids -out $R/BrainS

## 2.4 Make blast and filter results

blastp -num_threads $N -query $R/sequence-epitopes.fasta -db $R/BrainS -out $I/blast-epitopes-BrainS.txt -evalue $EVALUE -outfmt "6 qseqid qstart qend qlen sseqid sstart send slen evalue length nident mismatch gaps qcovs"
awk -v COV=$COVERAGE '{if ($14 > COV) { print }}' $I/blast-epitopes-BrainS.txt > $R/blast-epitopes-BrainS-filtered.txt

echo "Total number of valid alignments"
wc -l $R/blast-epitopes-BrainS-filtered.txt

echo "Average alignment size "
cut -f 1-3 $R/blast-epitopes-BrainS-filtered.txt | sort | uniq | awk 'BEGIN{n=0; t=0} { s=$3-$2; t=t+s; n++;} END {ave=t/n; print ave}' 

cut -f5 $R/blast-epitopes-BrainS-filtered.txt | sort | uniq > $R/blast-epitopes-BrainS-protein_id.txt
$S/filter_line.pl -f $D/hg38-Ensembl_101-protein_id-gene_name.txt -i $R/blast-epitopes-BrainS-protein_id.txt -c 1 > $R/blast-epitopes-BrainS-protein_id-gene_name.txt
cut -f2 $R/blast-epitopes-BrainS-protein_id-gene_name.txt | sort | uniq > $R/blast-epitopes-BrainS-gene_name.txt
echo "There was a match with this number of proteins: "
wc -l $R/blast-epitopes-BrainS-protein_id.txt
echo "Which correspond to this many genes: "
wc -l $R/blast-epitopes-BrainS-gene_name.txt

## 2.5 Calculate match with specific cell types

for CELL in neuron microglia oligodendrocyte astrocyte
	do
	echo "Matching proteins in $CELL"
	cat $R/blast-epitopes-BrainS-protein_id.txt $I/ids-proteins-${CELL}_differentiation-cell_surface.txt | sort | uniq -d | wc -l
done


# ------
# Step 3 -- Perform analysis of random Non BrainS proteins
# ------

echo ""
echo "------"
echo "Step 3 -- Perform analysis of random Non BrainS proteins"
echo "------"

## 2.1 Make a random selection of N proteins from the NO BrainS dataset (N= number of BrainS proteins)

echo "Making random sampling"

for COUNT in $(seq 1 $RANDOMN)
do 
	$S/random_fasta.pl $R/human-proteins-cell_surface-NO_BrainS.fasta $BRAINSN $NOBRAINSN > $I/sequence-proteins-cell_surface-NO_BrainS-$COUNT.fasta
	makeblastdb -dbtype prot -in $I/sequence-proteins-cell_surface-NO_BrainS-$COUNT.fasta -title NO_BrainS_random_$N -parse_seqids -out $I/NO_BrainS_random_$COUNT >> $I/makeblastdb_sampling.log
done

echo "Making blast of random sequences"

for COUNT in $(seq 1 $RANDOMN)
do
	blastp -num_threads $N -query $R/sequence-epitopes.fasta -db $I/NO_BrainS_random_$COUNT -out $I/blast-epitopes-NO_BrainS-$COUNT.txt -evalue $EVALUE -outfmt "6 qseqid qstart qend qlen sseqid sstart send slen evalue length nident mismatch gaps qcovs"
	awk -v COV=$COVERAGE '{if ($14 > COV) { print }}' $I/blast-epitopes-NO_BrainS-$COUNT.txt > $I/blast-epitopes-NO_BrainS-$COUNT-filtered.txt
	cut -f5 $I/blast-epitopes-NO_BrainS-$COUNT-filtered.txt | sort | uniq > $I/blast-epitopes-NO_BrainS-$COUNT-protein_id.txt
	wc -l $I/blast-epitopes-NO_BrainS-$COUNT-protein_id.txt >> $R/Random-NO_BrainS-Matches.txt
done
echo "Finished! Check the result of random sampling blasts in $R/Random-NO_BrainS-Matches.txt"

echo ""
echo "======"
echo "ALL DONE!"
echo "======"
echo ""
