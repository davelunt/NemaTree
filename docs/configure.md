# Configure the workflow

Configure the workflow by editing `config/config.yaml`

## sequences

You must specify your sample fasta file in config.yaml (REQUIRED).

```
samples:
  myseqs: "resources/samples/myseqs.fas"
```

Although technically you can list multiple files here under samples, you should ask yourself if that is really what you want to do. Files listed here will place sequences onto one tree per sample, not all into one tree. This workflow is not designed for processing many sequences (hundreds) it is designed differently. Evolutionary Placement Algorithm (EPA) might be a better approach.

Also see [sequence-prep.md](sequence-prep.md)

## Reference libraries

There are two reference sequence alignment files supplied in resourcfes/reference.

- `genus_ref148.fas` contains (N=148) sequences from species across the entire genus, and Pratylenchus outgroups.
- `ref148clades123.fas` contains a subset of the genus data consisting of only clade 1 (tropical apomicts), clade 2 (M. hapla group) and clade 3 (M. chitwoodi group). Two M. artiellia and two M. baetica are included as outgroups.

Choose whether you want to add sequences to the whole genus data (`clades123: FALSE`) or just clades 123 data (`clades123: TRUE`).

## Alignment plots and tables

Alignment plots can be deactivated here

CIAlign options are also here


## Tree contruction and rooting

See also [tree-formatting.md](tree-formatting.md)

The IQtree substitution model can be specified here. The default is GTR+R3 which was determined to be best fit by BIC. On slightly different data the model may vary slightly, but usually makes little difference.

You should change the tree rooting to match your analysis using TRUE and FALSE. Make sure only one outgroup option is labelled TRUE

If you are using the whole genus reference alignment, the tree will be rooted on Pratylenchus sequences as the outgroup. Use `outgroup_root: True`

If you are using the clades123 reference alignment, the tree will be rooted by using the outgroup clade containing M. artiellia and M. baetica. Use `outgroup_list: TRUE`

Changing these options should not require the entire workflow to be rerun. Delete the `results/reporting/toytree/myseqsname_mafft_cialign_iqtree.html` file and rerun the workflow to generate a new tree image with the new root from the previous IQ-tree treefile.
