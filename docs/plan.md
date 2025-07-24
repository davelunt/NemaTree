# plan for RKN-RRNA phylogenies

## data

- download RKN-RRNA sequences from SILVA
- wrangle names with a silva script I have
- convert to DNA
- plot length and exclude short sequences

## alignments

- add sequences with MAFFT to standard alignment
- trim alignment with trimAl
- check alignment with Amas

## phylogenies

- fasttree to detect weird sequences
- add weirdos to exclude list and delete from alignment by rerunning
- make phylogenies with IQTree
