# Phylogenetic analysis of Root-Knot Nematode 18S rRNA sequences

This reproducible workflow processes 18S rRNA sequences from Root-Knot Nematodes, including quality control, alignment, and reporting. The workflow makes use of an alignment of sequences from the diversity of Meloidogyne species.

## Workflow Overview

The user should provide fasta sequences in a file in the `resources/samples/` directory with the .fas file extension.

The workflow can be configured using the `config.yaml` file, where you can specify parameters such as the minimum sequence length and the reference alignment file.

The workflow will:

1. Perform quality control on the sequences
2. Align the sequences to the reference alignment
4. Build a maximum likelihood tree
5. Generate a tree image as an html file

## Reproducibility

The workflow is reproducible and self-documenting.

## Configuring the workflow

The workflow can be configured using the `config/config.yaml` file. You can specify parameters such as the reference alignment file, whether to exclude certain sequences, and how to root and colour the tree.

## Running the workflow

### Provide a single sequence file with .fas extension

Make sure you have provided (DNA not RNA) fasta sequences in a file in the `resources/samples/` directory with the `.fas` file extension. Using an informative short filename will help you keep track of your samples as it will be used throughout the workflow. Do not provide multiuple files, place all fasta records in one fasta file. 

Tip: At a terminal in the workflow directory, run: `cat resources/samples/*.fas > resources/samples/your_sample_name.fas` to combine all fasta files into one file.

### Check the config.yaml

This file should contain:

- the name of your `.fas` file containing your samples (REQUIRED)
- the name of the reference alignment file to which your sequences will be aligned
    - choose between the whole genus or just clades 1, 2, and 3
- rooting and colouring information for the tree

Except for the name of your sample file, all other parameters have default values and can be left as is.

### Dry run, then run the workflow

Begin with a dry run to check all files are present.

`snakemake -np`

If all is well, run the workflow with:

`snakemake --cores 4`

### common reasons for failure

#### wrong reference alignment name, or sample name

check this in config. fasta/fas, capitalisation, location

#### IQ-tree times out

It can take quite a while to construct the tree. Maybe a coupole of minutes, depending on data set and computer, and sankemake may time out after 30 seconds waiting for IQtree to write its files. Try
snakemake --cores 3 --latency-wait 300
this will ask snakemake to wait 300 seconds instead

#### wrong outgroups

toytree will complain and fgail if your outgroup taxon is not in your dataset