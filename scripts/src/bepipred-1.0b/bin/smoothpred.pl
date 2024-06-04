#!/usr/bin/perl -w

# smoothpred
# Jens Erik Pontoppidan Larsen
# 2004.05.17
# Applies a running averaging window to prediction data.

# New version with asymmetric windows in the beginning and the end of the file
# jepl 2004.10.21

#
# Import libraries
#
use Getopt::Std;		
use strict;				
use English;				

use vars qw($opt_h $opt_w $opt_e);
getopts('hw:e')||usage();

#
# usage prints a description of how to use the program
#
sub usage{
  print("Usage: $0 \[-h\] < inrocfile > outrocfile -w windowsize\n");
  print("Command line options:\n");
  print("	h: Print this meassage\n");
  print("	w: Size of smoothing window\n");
  print("	e: Go to the edges of the file and smooth with asymmetric windows\n");  
  exit;
}
#
# If -h option is used, print description of usage
#
if (defined($opt_h)) {usage()};


if (not defined($opt_w)) {die "Window size must be specified";} 

#

################################################################################
#
# Parse input
#
################################################################################
#

my @data;

my $windowsize = $opt_w;
my $halfwindow = ($windowsize-1)/2;
my $centerwindowpos = ($windowsize+1)/2;

# Parse indata
my $inline;
my $n = 0;
while($inline = <STDIN>)
{
	($data[$n][0], $data[$n][1]) = split " ", $inline;
	$n++;
}

# First column contains the target values. The second contains the predicted values.

my $NoOfData = $#data+1;

# print "No Of Data, $NoOfData\n";

# Main loop

my $m = 0;	#Counter for output array
my @outputdata;	#Array for output data.
my $windowsum;	# Temporary sum.
my $l;		# window counter

if (!defined($opt_e)) # No asymmetric windows at the edges of the file.
{


    for($n = $halfwindow; $n < $NoOfData- $halfwindow; $n++)
    {
	
	$windowsum = 0;
	for($l = 0; $l < $windowsize; $l++)
	{
	    $windowsum += $data[$n-$halfwindow+$l][1];
	}
	$outputdata[$m][1] = $windowsum/$windowsize;
	$outputdata[$m][0] = $data[$n][0];
	$m++;
    }

} else { # Asymmetric windows in the beginning and the end of the file
    
   # Treat the beginning of the file

    for($n = 0 ; $n < $halfwindow; $n++)
    {
    	$windowsum = 0;
	for($l = 0; $l < $n+$halfwindow+1;$l++)
	{
	    $windowsum += $data[$l][1];
	}
	$outputdata[$m][1] = $windowsum/($n+$halfwindow+1);
	$outputdata[$m][0] = $data[$n][0];
	$m++;
    }
   
   # Treat the middle 
    for($n = $halfwindow; $n < $NoOfData- $halfwindow; $n++)
    {
	
	$windowsum = 0;
	for($l = 0; $l < $windowsize; $l++)
	{
	    $windowsum += $data[$n-$halfwindow+$l][1];
	}
	$outputdata[$m][1] = $windowsum/$windowsize;
	$outputdata[$m][0] = $data[$n][0];
	$m++;
    }
   

    # Treat the end

    for($n = $NoOfData-$halfwindow ; $n < $NoOfData; $n++)
    {
    	$windowsum = 0;
	for($l = $n-$halfwindow; $l < $NoOfData;$l++)
	{
	    $windowsum += $data[$l][1];
	}
	$outputdata[$m][1] = $windowsum/($NoOfData-$n+$halfwindow);
	$outputdata[$m][0] = $data[$n][0];
	$m++;
    }
     
    
    
}
# Generate output

for($n = 0; $n < $m; $n++)
{
    print $outputdata[$n][0],"\t";
    printf "%1.5f\n", $outputdata[$n][1];
	
}
