#!/usr/bin/perl
use strict;

## Usage filter-peptides.pl FILE SCORE; SCORE is the minimum score

open (FILE, $ARGV[0]) || die "\nError: The file $ARGV[0] does not exist\n\n";

my $prot = "";
my $treshold = 1;
if ($ARGV[1]) {
	$treshold = $ARGV[1]; 
}

while (<FILE>){
	next if (/^Position/); #skip the header line
	if (/^input:\s(.+)/) { # save the name of the protein
		$prot = $1;
	} else {
		my @line = split(/\t/,$_); #split the line by tabs
		chomp($line[5]);
		if ($line[5] >= $treshold) { # if the score is greater than the threshold
			print "$prot\t$line[2]\t$line[3]\t$line[5]\n"; # print prot, start, end and score
		}
	}
}

close(FILE);
