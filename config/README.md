# Configure the workflow

Configure the workflow by editing `config.yaml`

You must include the basename of your .fas sequence file. e.g. seqs_to_add: "myseqsname" if `resources/samples/myseqsname.fas` is your sequence file

You may exclude any reference sequences from analysis by adding their names to `excluded.txt`

## sequence formatting

Make sure that you provide a single sequence file containing all the sequences you want to add to the reference alignment tree.

Sequences need to be DNA not RNA, and should be in fasta format with the `.fas` file extension.

Some fasta header cleanup is performed by the workflow, removing problematic characters and whitespace. Any name changes are documented in files in `results/reporting/validated/`

Using a short informative fasta header line for each sequence will help avoid issues. Very long fasta header lines will force the tree to be compressed.

## Tree rooting

You should change the tree rooting to match your analysis using TRUE and FALSE. Make sure only one outgroup option is labelled TRUE

If you are using the whole genus reference alignment, the tree will be rooted on Pratylenchus sequences as the outgroup. Use--> outgroup_root: True

If you are using the clades123 reference alignment, the tree will be rooted by using the outgroup clade containing M. artiellia and M. baetica. Use--> outgroup_list: TRUE

Whatever your reference alignment you can also choose midpoint rooting, which will root the tree at the midpoint of the longest branch. Use--> midpoint_root: TRUE

MAD rooting, a very good option, will root the tree using the Minimal Ancestor Deviation algorithm. Use--> mad_root: TRUE

Changing these options should not require the entire workflow to be rerun. Delete the `results/reporting/toytree/myseqsname_mafft_cialign_iqtree.html` file and rerun the workflow to generate a new tree image with the new root from the previous IQ-tree treefile.
