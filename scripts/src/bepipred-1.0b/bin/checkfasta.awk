#! /usr/freeware/bin/gawk -f

# This script does some checking on a fasta file.
# It converts non-amino acid characters to another character.


BEGIN {

   NON_PROT_ALPH	= "[^ACDEFGHIKLMNPQRSTVWY]";
   EXCHANGECHAR		= "A";
}
# FASTA entry header ==========================================================
/^>/ {
  print $1,$2;
  next;

}

/[^\^>]/{
# picking up FASTA sequence ===================================================

  # convert to upper-case and replace non-standard symbols ....................
  $1 = toupper($1);
  gsub(NON_PROT_ALPH,EXCHANGECHAR,$1);
  print $1;
  next;
}
