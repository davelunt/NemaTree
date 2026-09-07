# Tree Formatting

## I like the tree and want to save it as an image for a publication

Default output is html. Using the config you can also save in other file formats, eg .png, .pdf or .svg.

I have moved many image settings to the config file, investigate these. You will be able to change the colours, set the image size etc. I think you will have enough control to format a publication ready image.

If you need to make more modifications the best way to get complete control over formatting is to take the `results/iqtree/<sample_name>.treefile` produced by IQ-tree and to optimse it using toytree python package outside of the workflow.

Many options can be copied from `workflow/scripts/toytree_colours.py`, or you can use the toytree documentation at https://toytree.readthedocs.io

### Image size

You may need to increase the image height in the config file if you think the names are too squashed together.

`toytree_height: 1800`

You can change this and then delete the image to force snakemake to redo just the plotting. Or try `snakemake --cores 3 --force toytree_plot` to rerun just the plotting rule with the new config toytree_height.


## Tree rooting

You will need to choose the rooting method in config.yaml (and also the locus SSU/LSU)

Choose one of "outgroup", "outgroup_list", "midpoint", "mad".

I suggest:

| Scope       | Method        | Taxa                                       |
| ----------- | ------------- | ------------------------------------------ |
| genus       | outgroup      | outgroup_name: "Pratylenchus"              |
| clades123   | outgroup_list | list chosen automatically per locus        |


The config file gives you control of rooting your tree. If your chosen rooting methods fails it will try to midpoint root the tree. If you wish to try a different rooting method just delete the treefile and rerun snakemake (it won't redo all the steps, just recreate the tree diagram).

There is also rooting information in [configure.md](configure.md)


### Genus tree

If you are using the genus reference alignment I strongly recommend using the default rooting on Pratylenchus as outgroup.

Midpoint rooting and minimum ancestral deviation rooting produce suboptimal trees for SSU.


### Clades 123 tree

If you are building trees of clades 1,2 and 3 I would suggest using M.artiellia and M.baetica as outgroups. Outgroup list iof the exact tip names of these taxa are provided for SSU and LSU. The rooting will know which locus you have chosene in the config, and choose the appropriate oputgroup_list for that locus.

Midpoint rooting and minimum ancestral deviation (MAD) rooting produce good trees also.

## Bootstrap and other support values

These can be changed in the config file. Personally I don't believe these support values often tell us very much in an experiment adding new samples, and I prefer to leave them off the final tree.

There is a switch to turn off support values in config and `phylogenetic_support_values: False` will prevent them from being calculated and plotted.

`aLRT` is SH-like approximate likelihood ratio test. `ultrafast_bootstrap` is the ultrafast bootstrap approximation (UFBoot). Both are described in the IQtree documentation.

```
support_value_types:
    aLRT: 1000
    ultrafast_bootstrap: 1000
```

On the tree nodes they are plotted in the order aLRT/UFboot

To exclude one you could just comment out the line above. 1000 replicates, specified for both, is fairly standard but you can change the number if you wish.


## Relationships within clade 1

The relationships **within** clade 1 (tropical apomicts) are very unstable. I would not be confident about inferring too much here with either SSU or LSU rRNA dataset which have low diversity. Importantly, we would not (biologically) expect any single locus to accurately reflect the relationships for taxa that are from an allopolyploid radiation, phylogenomics seems to be the best approach.

Summary: this workflow is great at placing unknown RKN samples into a phylogenetic context, but the resolution of closely related species may need much more (carefully selected) data.
