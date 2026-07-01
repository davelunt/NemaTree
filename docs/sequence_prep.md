# preparing sequences to add

The workflow has quality control steps for the sequences to be added, but it is also important to prepare correctly.

Sequences need to be in a single `.fas` file in `resources/samples`. You will need to add the basename of this file to the `config/config.yaml` file (mysamples for mysamples.fas).

If you need to concatenate multiple fasta files into one, you can use the following command:

`cat *.fas* > mysamples.fas`

This will concatenate `.fas` and `.fasta` files but not `.fna` so long as you are in the same directory as the files. 

You must not have spaces in filenames that are going to be processed by a workflow. Use name_underscores or name-hyphens or camelCase instead.

## whitespace and 'poison characters'

The quality control will remove spaces in the fasta header and replace with underscores. Some other characters eg [:;()] are also replaced with underscores as they can interfere with some downstream tools as their meaning clashes with newick file syntax.

## Unique names

Sequences with identical names will be dropped from the analysis after the alignment. You can however use this command to add a unique number to the end of the header line. Make sure the conda environment is activated (to have Seqkit installed). This changes seqA to SeqA_001:

`seqkit replace -p $ -r "_{nr:03d}" mysamples.fas > mysamples_unique.fas`

## Good names

It is a good idea to think ahead and have short informative unique names for your sequences. Very long names can cause the tree to become compressed.

## minimum sequence lengths

The shorter your sequence the less information it contains and the less accurate will be its incorporation into the tree. Some sequences on GenBank are ~350bp, and this is the minimum you should consider. Sequences that are >900bp are much more robust and will give much more information. If you only want to know "is this a tropical apomict in clade 1, or not" then even short sequences will work. If you want to know something more subtle, then you will need longer sequences.

The config file has the ability for you to **not** add your sequences if they are below a certain length (enforce_minlength: True), and to specify what that minimum length is (min_seq_length: 500). Sometimes this is useful in cases where you want to investigate the precision of the results. The default is not to use this, which is best in most cases.
