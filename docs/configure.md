# Configure the workflow

Configure the workflow by editing `config/config.yaml`

## Sequences

You must specify your sample fasta file in config.yaml (REQUIRED).

```
samples:
  myseqs: "resources/samples/myseqs.fas"
```

Remember to change both the name (myseqs), and the filepath (resources/samples/myseqs.fas). The name is important because this is how all your output files will be labelled, so keep it short and without spaces in the name.

If you are working with both 18S/SSU and 26S/LSU sequences I highly recommend you incorporate this into the name (eg SSUexpt1) as mixing LSU and SSU seqs in the samples and reference will lead to hard-to-diagnose errors.

The `resources/samples` directory contains some test files you can use to get going.

Although technically you can list multiple files here under samples, you should ask yourself if that is really what you want to do. Files listed here will place sequences onto one tree per sample file, not all into one tree. This workflow is not designed for processing many sequences (hundreds) it is designed differently. Evolutionary Placement Algorithm (EPA) might be a better approach for hundreds of sequences.

Also see [sequence-prep.md](sequence-prep.md)


## Reference libraries

There are reference sequence alignment files supplied in resources/reference for both LSU and SSU.

- `SSU_genus_ref156.fas` contains (N=156) sequences from species across the entire genus, and Pratylenchus outgroups.
- `SSU_clades123_ref156.fas` contains a subset of the genus data (~N=122) consisting of only clade 1 (tropical apomicts), clade 2 (M. hapla group) and clade 3 (M. chitwoodi group) sensu Holterman et al (2009), de Ley et al (2002). Two M. artiellia and two M. baetica are included as outgroups.
- `LSU_genus_ref5.fasta` is the genus reference alignment for LSU sequences with Pratylenchus outgroups.
- `LSU_clades123_ref5.fasta` is the reference library for clades 123, with M. artiellia and M. baetica included as outgroups

The config file asks you to choose two things:
(1) Choose locus to analyse: "SSU" or "LSU"
locus: "SSU"

(2) Choose scope of the reference library: "genus" or "clades123"
scope: "genus"

Choose whether you want to add sequences to the whole genus data or just clades 123 data. Its probably best to start with the whole genus reference, and use clades123 reference when you know (roughly) what you are dealing with.

Given these two choices the workflow should select the correct reference library.

### Modifying reference alignments

Mostly you will just want to use the high quality reference alignments provided. You may however have new sequences from the databases, or your own sequences that you want to be part of a new reference.

The easiest way to do this could be to add those new sequences to the old reference alignment using this workflow, and then copy `results/cialign/{sample}_mafft_cialign_cleaned.fasta` to `resources/reference`, rename as your new reference alignment, and modify the config file to point at it.

### Creating clades123 from the genus reference

If you have a new genus reference file but wish a version appropriate for just clades123 you can generate this using seqkit:

`seqkit grep -f nonclades123.txt LSU_genus_refN.fasta -v -o LSU_clades123_refN.fasta`

`nonclades123.txt` is a file with fasta record names (no ">") to be excluded from the genus alignment (`LSU_genus_refN.fasta`) to create the clades123 alignment (`LSU_clades123_refN.fasta`). One record per line, no commas or other formatting. Suggested files for both SSU and LSU are included in the `/config` directory, but you should check carefully against the genus tree to make sure nothing has been missed.


**The Mali decision:** It is likely that the clade containing M.mali and relatives are closer to clades 123 than are M.artiellia and M.baetica. Should they be used as outgroup instead? Maybe, maybe not. I find that including this clade for SSU, or specifying it as the outgroup to clades 123, leads to less-resolved relationships within clades 123. To my eyes a more informative tree is generated **excluding these sequences** and rooting on M.artiellia and M.baetica. These taxa seem to have more influence on short sequences in the ingroup, pulling them to 'unresolved' locations. In an ideal world all data would be included, but where we have short sequences, or very closely related sequences, phylogenetic relationships can be easily disturbed. You can decide for yourself, and maybe play with minimum sequence lengths in the config, but I usually retain all sequences for the genus level tree and exclude this group when using the clades 123 reference.


## Alignment plots and tables

Alignment plots can be deactivated in the config file using `generate_seq_plots: False`


## Minimum sequence length in the alignment

CIAlign options to length filter are also in config. This will reduce the number of taxa in the tree, but increase the quality of the phylogeny. 

```yaml
cialign_len_filter: True # Filter short sequences from alignment
cialign_minlen: 700 # minimum sequence length (bp)
```

The length filter should probably be smaller for LSU than SSU, but you can modify values and investigate.

If there are sequences you want to keep despite their length, put their names, one per line, in `retain_short_list: "config/retain_short_list.txt"`

`config/retain_short.txt` must exist if you are removing short sequences from the alignment with CIAlign ie `cialign_len_filter: True` in config. If the file is empty, no sequences will avoid the filter. If the file does not exist, the workflow will likely crash when you have `cialign_len_filter: True`. An empty `retain_short.txt` is provided in the config directory, do not to delete it.


## Tree contruction and rooting

See also [tree-formatting.md](tree-formatting.md)

The IQtree substitution model can be specified here. The default is GTR+R3 which was determined to be best fit for SSU reference alignment by BIC. For LSU the best fit model was TIM3+F+G4. On slightly different data the model may vary slightly, but usually makes little difference. Using GTR+I+G is a good option for most datasets.

### My Rooting Recommendations:

You will need to choose the rooting method:

Choose one of "outgroup", "outgroup_list", "midpoint", "mad". If rooting fails it will try to midpoint root the tree.

I suggest:

| Scope      | Method | Taxa |
| ----------- | ----------- | --------------------------- |
| genus      | outgroup       | outgroup_name: "Pratylenchus" |
| clades123   | outgroup_list        | list chosen automatically per locus |

The `outgroup` and `outgroup_list` are specified in the config file.

`outgroup` looks for the specified text in tip names ('Pratylenchus') rather than needing an exact tip name.

`outgroup_list` does need a list of exact tip names.

Changing these rooting options should not require the entire workflow to be rerun. Delete the `results/reporting/toytree/myseqsname_mafft_cialign_iqtree.html` file and rerun the workflow to generate a new tree image with the new root using the previous IQ-tree treefile.

Or you could try `snakemake --cores 3 --forcerun toytree_plot` to just rerun the plotting.


## References

De Ley et al. Phylogenetic Analyses of Meloidogyne Small Subunit rDNA. J Nematol. 2002;34: 319–327

Holterman et al. Small subunit rDNA-based phylogeny of the Tylenchida sheds light on relationships among some high-impact plant-parasitic nematodes and the evolution of plant feeding. Phytopathology. 2009;99: 227–235. doi:10.1094/PHYTO-99-3-0227
  