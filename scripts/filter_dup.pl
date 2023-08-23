#!/usr/bin/perl
use strict;

# This script will merge lines with a shared sequence and report the sequences in fasta format

## Usage filter_dup.pl TAB DUP; TAB is a file that contains IDs and sequences, tab separated. DUP is the file that contains duplicated sequences


my %dups=();

open (FILE, $ARGV[1]) || die "\nError: The file $ARGV[1] does not exist\n\n"; 

# Save the duplicated sequences in a hash
while (<FILE>){
	chomp;
	$dups{$_}="";
}
close(FILE);


# Open the tab file, search which sequences match with the dup, and stich the id together.

open (FILE, $ARGV[0]) || die "\nError: The file $ARGV[0] does not exist\n\n"; 
while (<FILE>){
	my @line = split(/\t/,$_); #split the line by tabs
	chomp($line[1]); # Delete \n
	my @ID = split(/\:/,$line[0]); #FastafromBed prints the id and the position of the sequence separated by :. We split the line to save the id
	if (exists $dups{$line[1]}) { # If the sequence is duplicated
		if ($dups{$line[1]}) { $dups{$line[1]} .= "|"; } # If there was a previous id, add a separator
		$dups{$line[1]} .= $ID[0]; #Concatenate the id
	} else { # If the sequence is not duplicated, print it
		print ">$ID[0]\n$line[1]\n";
	}
}
close(FILE);

# Finally, print the duplicated entries
foreach my $seq (keys %dups) {
	print">$dups{$seq}\n$seq\n";
}