#! /usr/bin/gawk -f

# mkgff
# 
# This script generate BepiPred 1.0 output in GFF. The input is the raw
# prediction output in the form:
# 
# 	<seqname>   <res #>   <res>   <score>
# 
# The external variables:
# 
# 	N	sequence number
# 	S	flag: include input sequence
# 	T	threshold for yes
# 	V	version of BepiPred
# 
# This script has to be run from the tmp directory as it assumes the existence
# if the input data.
# 
# VERSIONS	2006 Aug  4	launch, K. Rapacki
# 

BEGIN {	# sequence name
	cmd = ("cat seq." N ".fsa");
	cmd | getline;
	seqname = substr($1,2);
	print "##Type Protein",seqname;

	# sequence
	if (S) {
	   print "##Protein",seqname,cmd;
	   while (cmd | getline)
	         print "##" $0;
	   close(cmd);
	   print "##end-Protein";
	}

	# table header
	printf("# seqname            source        feature      ");
	print "start   end   score  N/A   ?";
	printf("# ----------------------------------------------");
	print "-----------------------------";
}

{
  printf("%-20s bepipred-%s epitope      %5d %5d  %6.3f  . .",$1,V,$2,$2,$4);
  if ($4>=T)
     printf("   E\n");
  else
     printf("   .\n");
}

# end of file
