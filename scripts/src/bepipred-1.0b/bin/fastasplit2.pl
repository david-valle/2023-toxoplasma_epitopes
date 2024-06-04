#!/usr/bin/perl -w
#
# Fasta splitter jepl version
# Splits a fasta file into fasta files, that only contain one sequence. 
# The names of the files are given by the number of the sequence.


# Import libraries
#
use Getopt::Std;			# Command line options
use strict;				# Strict parsing
use English;				# Allow use of long names (Camel p. 127)

use vars qw($opt_h ); 
getopts('h')||usage();
                   
#
# usage prints a description of how to use the program
#
sub usage{
  print("Usage: $0 \[-h\] < input_fasta_file\n");
  print("Makes a lot of fasta files in the directory containing only one sequence.\n");
  print("Command line options:\n");
  print("	h: Print this message\n");
  exit;
}
#
# If -h option is used, print description of usage
#
if (defined($opt_h)) {usage()};

# Parse input

my $bFileOpen = "false";
my $sInLine;
my $sSeqName;
my $sSeqTemp;
my $nSeqNumber = 0;

while($sInLine = <STDIN>)
{

    if($sInLine =~ /^\>/)
    {
    	if($bFileOpen eq "true")
	{
	    close OUT;
	}
	$nSeqNumber++;
    	open (OUT, ">seq.$nSeqNumber.fsa");
	$bFileOpen = "true";
    }
 
    print OUT $sInLine;
       

}
if($bFileOpen eq "true")
{
    close OUT;
}

print "Number of fasta files: $nSeqNumber \n";
