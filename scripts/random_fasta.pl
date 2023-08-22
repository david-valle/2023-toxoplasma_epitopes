#!/usr/bin/perl
use strict;

## Usage random_fasta.pl FASTA N TOTAL; N is the number of (random) chosen sequences, TOTAL is the total number of sequences

if ($#ARGV < 2) {
	print "This program randomly chooses N sequences from a multifasta file\n\nUsage: random_fasta.pl FILE.fa N TOTAL\n\nFILE.fa\tThe name of your fasta file\nN:\tThe number of random sequences you want to choose\nTOTAL:\tThe number of total sequences in your fasta file\n\n";
	exit(1);
}

my %hash=();
my $n = 0;
my $target = $ARGV[1];
my $tot = $ARGV[2];
my $rand = 0;

if (!$target) { die "\nError: the number of randomly chosen sequences must be greater than 0\n\n";}
if ($target < 1) { die "\nError: the number of randomly chosen  sequences must be greater than 0\n\n";}
if (!$tot) { die "\nError: the number of total sequences must be greater than 0\n\n";}
if ($tot < 1) { die "\nError: the number of total sequences must be greater than 0\n\n";}
if ($target > $tot) {die "\nError: the number of randomly chosen sequences can't be greater than the total number of sequences\n\n";}

while ($n < $target){
	$rand = int(rand($tot));
	if (!exists $hash{$rand}){
		$hash{$rand}=1;
		$n++;
	}
}



open (FILE, $ARGV[0]) || die "\nError: The file $ARGV[0] does not exist\n\n";

my $flag=0;
$n=0;

while (<FILE>){
	if(/^>/){
		if (exists $hash{$n}) {$flag =1; } else {$flag =0;}
		$n++;
	}
	if ($flag){print $_;}
}

close(FILE);