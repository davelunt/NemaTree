# Configure the workflow

Configure the workflow by editing `config/config.yaml`

## Sequences

You must specify your sample fasta file in config.yaml (REQUIRED).

```
samples:
  myseqs: "resources/samples/myseqs.fas"
```

Although technically you can list multiple files here under samples, you should ask yourself if that is really what you want to do. Files listed here will place sequences onto one tree per sample, not all into one tree. This workflow is not designed for processing many sequences (hundreds) it is designed differently. Evolutionary Placement Algorithm (EPA) might be a better approach.

Also see [sequence-prep.md](sequence-prep.md)


## Reference libraries

There are two reference sequence alignment files supplied in resources/reference.

- `genus_ref145.fas` contains (N=145) sequences from species across the entire genus, and Pratylenchus outgroups.
- `ref145clades123.fas` contains a subset of the genus data (~N=122) consisting of only clade 1 (tropical apomicts), clade 2 (M. hapla group) and clade 3 (M. chitwoodi group). Two M. artiellia and two M. baetica are included as outgroups.

Choose whether you want to add sequences to the whole genus data (`clades123: FALSE`) or just clades 123 data (`clades123: TRUE`).

### Modifying reference alignments

Mostly you will just want to use the high quality reference alignments provided. You may however have new sequences on the databases, or your own sequences that you wanto to be part of a new reference.

The easiest way to do this could be to add those new sequences to the old reference alignment using this workflow, and then copy `results/cialign/{sample}_mafft_cialign_cleaned.fasta` to `resources/reference`, rename as your new reference alignment, and modify the config file to point at it.

### Creating clades123 from the genus reference

If you have a new genus reference file but wish a version appropriate for just clades123 you can generate this using seqkit:

`seqkit grep -v -n -f nonclades123.txt genus_refNNN.fas > clades123_genusNNN.fas`

`remove_nonclades.txt` is a file with fasta record names (no ">") to be excluded from the genus alignment (`genus_refNNN.fas`) to create the clades123 alignment (`clades123_genusNNN.fas`). One record per line, no commas or other formatting.

An example list can be found in `config/nonclades123.txt`. This needs to be carefully checked against your full genus tree to make sure it contains all the sequences you wish to exclude.

**The Mali decision:** It is likely (but not certain) that the clade containing M.mali and relatives are closer to clades 123 than are M.artiellia and M.baetica. Should they be used as outgroup instead? Maybe, maybe not. I find that including this clade, or specifying it as the outgroup to clades 123, leads to less-resolved relationships within clades 123. To my eyes a more informative tree is generated **excluding these sequences** and rooting on M.artiellia and M.baetica. Thesed taxa seem to have more influence on short sequences in the ingroup, pulling them to 'unresolved' locations. In an ideal world all data would be included, but where we have short sequences, or very closely related sequences, phylogenetic relationships can be easily disturbed. This workflow was designed for utility rather than 'ultimate truth'. You can decide for yourself, but I usually retain all sequences for the genus level tree and exclude this group as described above for clades 123.


## Alignment plots and tables

Alignment plots can be deactivated in the config file using `generate_seq_plots: False`

### Minimum sequence length in alignment

CIAlign options to length filter are also in config. This will reduce the number of taxa in the tree, but increase the quality of the phylogeny.

```
cialign_len_filter: True # Filter short sequences from alignment
cialign_minlen: 500 # minimum sequence length (bp)
```

If there are sequences you want to keep despite the length put their names, one per line, in `retain_short_list: "config/retain_short_list.txt"`

`config/retain_short.txt` must exist in this folder if you are removing short sequences from the alignment with CIAlign ie `cialign_len_filter: True` in config. If the file is empty, no sequences will avoid the filter. If the file does not exist, the workflow will crash when `cialign_len_filter: True`

## Tree contruction and rooting

See also [tree-formatting.md](tree-formatting.md)

The IQtree substitution model can be specified here. The default is GTR+R3 which was determined to be best fit by BIC. On slightly different data the model may vary slightly, but usually makes little difference.

You should change the tree rooting to match your analysis using TRUE and FALSE. Make sure only one outgroup option is labelled TRUE

If you are using the whole genus reference alignment, the tree will be rooted on Pratylenchus sequences as the outgroup. Use `outgroup_root: True`

If you are using the clades123 reference alignment, the tree will be rooted by using the outgroup clade containing M. artiellia and M. baetica. Use `outgroup_list: TRUE`

Changing these options should not require the entire workflow to be rerun. Delete the `results/reporting/toytree/myseqsname_mafft_cialign_iqtree.html` file and rerun the workflow to generate a new tree image with the new root from the previous IQ-tree treefile.
