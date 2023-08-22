#!/bin/bash

# By running this script you can fully replicate the results from our paper
# See Readme.md for more info

# Step 0 create intermediates and results dirs
mkdir -p inetermediates
mkdir -p results

# Step 1 -- Predict epitopes
for M in Chou-Fasman Emini Karplus-Schulz Kolaskar-Tongaonkar Parker
do
     predict_antibody_epitope.py -m $M -f data/T_gondii_RH88-genes.fasta > intermediates/out-${M}.txt
done
