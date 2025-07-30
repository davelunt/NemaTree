# Phylogenetic analysis of Root-Knot Nematode 18S rRNA sequences

This workflow processes 18S rRNA sequences from Root-Knot Nematodes, including quality control, alignment, and reporting. The workflow makes use of an alignment of sequences from the diversity of Meloidogyne species.

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

The workflow can be configured using the `config/config.yaml` file. You can specify parameters such as the minimum sequence length, the reference alignment file, and whether to exclude certain sequences.

## Running the workflow

Make sure you have provided fasta sequences in a file in the `resources/samples/` directory with the .fas file extension. Using an informative short filename will help you keep track of your samples as it will be used throughout the workflow

Begin with a dry run to check all files are present.

`snakemake -np`

If all is well, run the workflow with:

`snakemake --cores 4`



