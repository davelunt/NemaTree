# Snakemake workflow: RKN-rRNA

[![Snakemake](https://img.shields.io/badge/snakemake-≥6.3.0-brightgreen.svg)](https://snakemake.github.io)
[![GitHub actions status](https://github.com/davelunt/RKN-rRNA/workflows/Tests/badge.svg?branch=main)](https://github.com/davelunt/RKN-rRNA/actions?query=branch%3Amain+workflow%3ATests)

> **Warning**
> Please use git branches for all changes

A Snakemake workflow for phylogenetic analysis of root-knot nematode rRNA sequences

These analyses run as a snakemake workflow to ensure ease and reproducibility.

## Usage

The workflow is controlled by editing the `config.yaml` file in the config directory

Decide if you (a) wish to add new sequences to a RKN rRNA phylogeny or (b) wish a phylogenetic analysis of the reference alignment that represents teh diversity of Meloidogyne species.

## Prepare the environment

Open a terminal and navigate to the directory containing the workflow (probably called RKN-RRNA)

The computational environment (all the sioftware required for the analyses) is specified in `workflow/envs/environment.yaml`

Make sure you have miniconda installed. See instructions at the website https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html

Build the environment using conda `conda env create -f envs/environment.yaml` and `conda activate rknrrna`

Installing and using mamba may increase the speed of creating the environment. Although slow, creating this environment only needs to be done once per machine, not each time the workflow is run.

## Add new sequences

Prepare your sequences as a single fasta file in `resources/samples` with the `.fas` extension (if you use `.fasta` you will have to edit the first rule to expect this extension).

Edit the `config.yaml` to make sure it says `add_sequences: TRUE` and `ref_only: FALSE` and specifies the name of your sequences-to-be-added file without the .fas extension eg `seqs_to_add: "my_new_sequences"`

## Run the workflow

`snakemake -np` will perform a dry run of the analysis. It will catch most, but not all issues.

`snakemake --cores 3 --wait-latency 300` will be a good starting point to run the analysis

The reference alignment has about 150 sequences in an alignment of approximately 1800bp. When adding about 20 new sequences it runs in about 2 minutes with 3 cores on a basic laptop (M2 MacBook Air with 4 cores and 8G of RAM).

`--wait-latency 300` is specified because IQtree takes longer than 30 seconds (snakemake's default wait period) to complete the analysis and write the files. Giving it a maximum wait of 5 minutes is safer.

## Examine the results

The final phylogenetic tree diagram is found in `results/reporting/toytree`as an html file. Since it is an svg file embedded in the html page you should be able to zoom in as required.

There are extensive other characterisations of the data, mostly in the `results/reporting` directory.

### Altering and re-running

If you wish to alter the tree, perhaps removing taxa, and/or rerooting this can be done without running the entire workflow. Transfer the cialign output alignment (from which the tree was built) to the `resources/reference` directory and change the config to make it the new reference library. Remove sequences if required. Specify a different root in `workflow/scripts/toytreref.py` should you wish. Change the config to  `add_sequences: FALSE` and `ref_only: TRUE` then you c an run snakemake as before but it will only run IQtree (phylogeny building) and Toytree (tree figure creation).

If you wish to alter the colour scheme you can edit the `workflow/scripts/toytreref.py` script as required. If you want to avoid this altogether try `tip_labels_colors="black",` rather than `=colorlist`.

## Reproducibility

The analysis should be completely reproducible if the `RKN-RRNA` working directory is shared. The `workflow/envs/environment.yaml` file will specify all required software. The reference alignment and any added sequences are found in the `/resources` directory, all parameters are recorded in the config.yaml or the rules themselves. Results and all intermediate files are deposited in the `/results` directory.

The entirity of the workflow, including data and results, can be archived with `snakemake --archive my-workflow.tar.gz` and uploaded to a sharing platform like Zenodo.org to generate a doi you can cite in your manuscript.

## Example Methods Text

A very minimal Methods section describing basic use of this workflow might be as follows:

Phylogenetic analysis of root-knot nematode SSU rRNA sequences was carried out with the RKN-RRNA Snakemake workflow, available 

## Citations

You should cite the papers of the analysis software used in this workflow if you publish your use of the workflow:
Snakemake:
Seqkit
IQtree
Toytree
CIAlign
AMAS
MAFFT

