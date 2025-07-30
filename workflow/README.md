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