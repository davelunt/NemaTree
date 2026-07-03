# Tree Formatting

## I like the tree and want to save it as an image for a publication

The best way to get complete control is to take the results/iqtree/<sample_name>.treefile produced by IQ-tree and to optimse it using toytree outside of the workflow.

You can save it as a graphics format such as .png or .svg
You can change the colours
You can set the image size

Many options can be copied from `workflow/scripts/toytree.py`, `.../toytreref.py` or you can use the toytree documentation at https://toytree.readthedocs.io

## Tree rooting

The config file gives you control of rooting your tree. If your chosen rooting methods fails it will try to midpoint root the tree. If you wish to try a different rooting method just delete the treefile and rerun snakemake (it won't redo all the steps, just recreate the tree diagram).

NB you can only specify one rooting method (one option as TRUE). If you specify more than one you will get this error:

`ValueError: Config error: Exactly one of rooting.outgroup_root, rooting.outgroup_list, rooting.midpoint_root, or rooting.mad_root must be True.`

### Genus tree

If you are using the genus reference alignment I strongly recommend using the default rooting on Pratylenchus as outgroup.

```
  outgroup_root: True
  outgroup_name: "Pratylenchus"
```

Midpoint rooting and minimum ancestral deviation rooting produce suboptimal trees.

### Clades 123 tree

If you are building trees of clades 1,2 and 3 I would suggest using M.artiellia and M.baetica as outgroups.

```
  outgroup_list: True
  outgroup_list_names: # root on ancestral node of these taxa, exact names should be used
    - "M_artiellia_AF442192"
    - "M_baetica_KP896296"
```

Midpoint rooting and minimum ancestral deviation (MAD) rooting produce good trees also.

## Relationships within clade 1

The relationships **within** clade 1 are very unstable. I would not be confident about inferring too much here with this SSU-rRNA dataset which has low diversity. We would not (biologically) expect any single locus to accurately reflect the relationships for taxa that are allopolyploids, phylogenomics seems to be the best approach.

Summary: this workflow is great at placing unknown RKN samples into a phylogenetic context, but the resolution of closely related species may need more (carefully selected) data.
