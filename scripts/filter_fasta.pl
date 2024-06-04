#!/usr/bin/perl
use strict;

# This program includes or excludes the sequences of a fasta file based on a list of sequences ids given by the user

## Usage filter_fasta.pl FASTA LIST_ID [-e]; FASTA is the fasta file | LIST_ID is the list of ids  | -e if you want to EXCLUDE the sequences matching LIST_ID (by default the program will include the sequences) 

my $include = 1; # Turn on include flag

if ($ARGV[2] eq "-e") { # If the use wants to exclude
	$include = 0; # Turn off include flag
}

open (FILE, $ARGV[1]) || die "\nError: The file $ARGV[1] does not exist\n\n";

my %hash=();

while (<FILE>){
	chomp;
	$hash{$_}=1;
}

close(FILE);

open (FILE, $ARGV[0]) || die "\nError: The file $ARGV[0] does not exist\n\n";

my $flag=0;

while (<FILE>){
	if(/^>(.+)/){
		chomp($1);
		if ($include){
			if (exists $hash{$1}) {$flag =1;} else {$flag =0;}
		} else {
			if (exists $hash{$1}) {$flag =0;} else {$flag =1;}
		}
		
	}
	if ($flag){print $_;}
}

close(FILE);