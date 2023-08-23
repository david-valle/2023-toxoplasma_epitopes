#!/bin/bash

# By running this script you can fully replicate the results from our paper
# See Readme.md for more info

# Set environment variables

## Folders
I=intermediates ### Here you will save the intermediate files. Modify if needed
R=results ### Here you will save the final results. Modify if needed
S=scripts ### This folder contains the scripts needed to run the analysis

## Files 

FASTA="data/T_gondii_RH88-genes.fasta"  ### Note: If you just want to try the analysis, replace this line with: FASTA="data/test.fasta"

## Methods

METHODS="Chou-Fasman Emini Karplus-Schulz Kolaskar-Tongaonkar Parker" ### You can edit this list to modify the methods used for peptide prediction

# Step 0 create intermediates and results directories

mkdir -p $I
mkdir -p $R

# Step 1 -- Predict, filter and merge epitopes

## 1.1 Predict epitopes with all 5 algorithms

for M in $METHODS
do
     predict_antibody_epitope.py -m $M -f $FASTA > $I/out-$M.txt
done

echo "Total predicted peptides per method"
wc -l $I/out-*.txt

## 1.2 FIlter the results with a score greater or equal than 1 and write a bed file

SCORE=1 ### Modify for different score stringencies

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

cat $I/merged-*.bed | sortBed -i - | mergeBed -c 4 -o mean -i - > $R/merged-all_methods.bed

echo "Total merged peptides between all methods"
wc -l $R/merged-all_methods.bed

## 1.6 Calculate average size for all methods

echo "Average peptide size for all methods"
awk 'BEGIN{n=0; t=0} { s=$3-$2; t=t+s; n++;} END {prom=t/n; print prom}' $R/merged-all_methods.bed


## 1.6 Get sequences for merged peptides

fastaFromBed -fi $FASTA -fo $I/sequence-all_methods.tab -bed $R/merged-all_methods.bed -tab

## 1.7 Merge duplicated sequences

cut -f2 $I/sequence-all_methods.tab | sort | uniq -d > $I/temp
$S/filter_dup.pl $I/sequence-all_methods.tab $I/temp > $R/sequence-all_methods.fasta
rm $I/temp
echo "Total non-redundant peptide sequences"
grep ">" $R/sequence-all_methods.fasta | wc -l

# Step 2 -- Predict, filter and merge epitopes
