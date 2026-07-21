# Reference alignments and sequence alignments

## Reference alignments

The reference alignment must be specified in the config.yaml file

## Duplicate names

If you add a sequence with a name that is already in the reference alignment, it will be dropped from the analysis. This is probably what you want.

There is currently no easy way to fix this in the workflow, since it is an edge case that you will want to retain these. Should you wish to keep these you can use Seqkit to add a unique counter to duplicated names, as described in the [sequence preparation](sequence_prep.md) section. You will need to run this on the initial mafft alignment `results/mafft/{sample}_mafft.fas` then delete all later (downstream)files in the results directory and re-run the workflow. This will re-run the alignment with the new unique names.

## Removing outlier sequences

Sometimes sequences are aligned but you can see that they are not really aligned at all. We attmept to drop very divergent sequences from the alignment using `rule CIAlign_remove_divergent_trim:` You can get a description of how this is done at the [CIAlign website](https://github.com/KatyBrown/CIAlign). This rule also trims alignment ends, which can be a source of variability not reflecting real phylogeny.

## Reporting

Both AMAS and CIAlign produce reports on the alignment in `results/reporting/amas` and `results/reporting/cialign`. The AMAS report is a tabular `.tsv` file with infomration on the alignment. CIALIGN produces many plots and information on the alignment. Some of these are suppressed in the config file with `generate_seq_plots: False` as it can increase the time for the workflow to run (slightly) and may be unnecesary when investigating the analysis.

## Alignment processing sequence

1. add sample seqs to ref alignment -->`results/mafft/{sample}_mafft.fas`
2. remove duplicate names --> `results/mafft/{sample}_mafft_nodups.fas`
3. remove divergent seqs and trim ends --> `results/cialign/{sample}_mafft_cialign_cleaned.fasta`
4. IQtree --> `results/iqtree/{sample}_mafft_cialign_cleaned_iqtree.treefile`
5. toytree --> `results/reporting/toytree/{sample}_mafft_cialign_cleaned_iqtree.html`

