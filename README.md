# Snakemake workflow: RKN-rRNA

[![Snakemake](https://img.shields.io/badge/snakemake-≥6.3.0-brightgreen.svg)](https://snakemake.github.io)
[![GitHub actions status](https://github.com/davelunt/RKN-rRNA/workflows/Tests/badge.svg?branch=main)](https://github.com/davelunt/RKN-rRNA/actions?query=branch%3Amain+workflow%3ATests)

> **Warning**
> Please use git branches for all changes

### A Snakemake workflow for phylogenetic analysis of root-knot nematode SSU rRNA sequences

These analyses run as a [snakemake workflow](https://snakemake.github.io/) to ensure ease and reproducibility.

This software is released under a permissive MIT license (see `LICENSE` file) and you may use and modify it as you wish. It would be helpful if you would acknowledge the source in any publication.

Lunt DH. RKN-RRNA: Analysis workflow for root-knot nematode rRNA. Github; Available: https://github.com/davelunt/RKN-RRNA

## Usage

Download the repository from GitHub to your local environment: `git clone https://github.com/davelunt/RKN-RRNA.git`

The workflow is controlled by editing the `config.yaml` file in the config directory

Decide if you (a) wish to add new sequences to a RKN rRNA phylogeny or (b) wish a phylogenetic analysis of the reference alignment that represents the diversity of Meloidogyne species.

## Prepare the environment

Open a terminal and navigate to the directory containing the workflow (probably called RKN-RRNA)

The computational environment (all the software required for the analyses) is specified in `workflow/envs/environment.yaml`

Make sure you have miniconda installed. See instructions at the website https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html

Build the environment using conda `conda env create -f envs/environment.yaml` and `conda activate rknrrna`

Installing and using [mamba](https://github.com/mamba-org/mamba) may increase the speed of creating the environment. Although slow, creating this environment only needs to be done once per machine, not each time the workflow is run.

If you skip this conda environment step Snakemake should create the conda environment automatically when you run the workflow. It will take longer the first time you run the workflow, as this includes software installation, but be much faster thereafter.

## Add new sequences

Prepare your sequences as a single fasta file in `resources/samples` with the `.fas` extension (if you use `.fasta` you will have to edit the first rule to expect this extension).

Edit the `config.yaml` to make sure it says `add_sequences: TRUE` and `ref_only: FALSE` and specifies the name of your sequences-to-be-added file without the .fas extension eg `seqs_to_add: "my_new_sequences"` if you have a file called `my_new_sequences.fas` in the `resources/samples` directory.

## Run the workflow

`snakemake -np` will perform a dry run of the analysis. It will catch most, but not all issues.

If the dry run doesn't flag errors then run the analysis with `snakemake --cores 3 --wait-latency 300`

The reference alignment has about 150 sequences in an alignment of approximately 1800bp. When adding 20 new sequences it runs in about 2 minutes with 3 cores on a basic laptop (M2 MacBook Air with 4 cores and 8G of RAM).

`--wait-latency 300` is specified because IQtree takes longer than 30 seconds (Snakemake's default wait period) to complete the analysis and write the files. Giving it a maximum wait of 5 minutes (300 seconds) is safer.

## Examine the results

The final phylogenetic tree diagram is found in `results/reporting/toytree`as an html file. Since it is an svg file embedded in the html page you should be able to zoom in as required.

There are extensive characterisations of the data, mostly in the `results/reporting` directory.

### Altering and re-running

If you wish to alter the tree, perhaps removing taxa, and/or rerooting this can be done without running the entire workflow. Transfer the cialign output alignment (from which the tree was built) to the `resources/reference` directory and change the config to make it the new reference library.

Remove sequences if required. If you routinely wish to remove the same sequences, for example removing all the sequences except certain clades, one strategy is to list the names of all the sequences to remove in a `remove_list.txt` file. You can then use seqkit to remove them and save a new file with a command like `seqkit grep -v -n -f remove_list.txt ref_alignment.fas > ref_alignment_small.fas`. It is recommended to work on a copy of your reference alignment.

You can specify a different root for the phylogeny in `workflow/scripts/toytreref.py`. Change the config to `add_sequences: FALSE` and `ref_only: TRUE` then you can run snakemake as before but it will only run IQtree (phylogeny building) and Toytree (tree figure creation).

If you wish to alter the colour scheme you can edit the `workflow/scripts/toytreref.py` script as required. If you want to avoid this altogether try `tip_labels_colors="black",` rather than `=colorlist`.

## Reproducibility

The analysis should be completely reproducible if the `RKN-RRNA` working directory is shared. The `workflow/envs/environment.yaml` file will specify all required software. The reference alignment and any added sequences are found in the `/resources` directory, all parameters are recorded in the `config.yaml` or the rules themselves. Results and all intermediate files will have been deposited in the `/results` directory.

The entirity of the workflow, including data and results, can be archived with `snakemake --archive my-workflow.tar.gz` and uploaded to a sharing platform like [Zenodo.org](https://zenodo.org) to generate a doi you can cite in your manuscript.

## Example Methods Text

A very minimal manuscript Methods section describing basic use of this workflow might be as follows:

Phylogenetic analysis of root-knot nematode SSU rRNA sequences was carried out with the RKN-RRNA workflow (Lunt 2025). The workflow uses Snakemake (Mölder et al 2021) to implement the entire analysis using a computational environment specified in the `workflow/envs/environment.yaml` file. A reference alignment of diverse root-knot nematode SSU rRNA sequences, selected for species representation and length, and aligned with MAFFT (Nakamura et al. 2018), was used for comparison and is made available in the repository `/resources` directory. The workflow uses MAFFT to add user-provided SSU sequences to this reference alignment, Seqkit (Shen et al. 2016) to report on sequence data, CIAlign (Tumescheit et al. 2022) for alignment cleaning and reporting, AMAS (Borowiec 2016) for alignment reporting, IQtree (Nguyen et al 2014) for phylogenetic analysis, and Toytree (Eaton 2020) for tree visualisation. All further details of program versions, parameters, and sequences used are recorded in the reproducible workflow repository.

## Citations

You should cite the papers of the analysis software used in this workflow if you publish your use of the workflow:

Borowiec ML. AMAS: a fast tool for alignment manipulation and computing of summary statistics. PeerJ. 2016;4: e1660. doi:10.7717/peerj.1660

Eaton DAR. Toytree: A minimalist tree visualization and manipulation library for Python. Matschiner M, editor. Methods Ecol Evol. 2020;11: 187–191. doi:10.1111/2041-210X.13313

Lunt DH. RKN-RRNA: Analysis workflow for root-knot nematode rRNA. Github; Available: https://github.com/davelunt/RKN-RRNA

Mölder F, Jablonski KP, Letcher B, Hall MB, Tomkins-Tinch CH, Sochat V, et al. Sustainable data analysis with Snakemake. F1000Res. 2021;10: 33. doi:10.12688/f1000research.29032.1

Nakamura T, Yamada KD, Tomii K, Katoh K. Parallelization of MAFFT for large-scale multiple sequence alignments. Bioinformatics. 2018;34: 2490–2492. doi:10.1093/bioinformatics/bty121

Nguyen L-T, Schmidt HA, von Haeseler A, Minh BQ. IQ-TREE: A fast and effective stochastic algorithm for estimating maximum likelihood phylogenies. Mol Biol Evol. 2014. doi:10.1093/molbev/msu300

Shen W, Le S, Li Y, Hu F. SeqKit: A Cross-Platform and Ultrafast Toolkit for FASTA/Q File Manipulation. PLoS One. 2016;11: e0163962. doi:10.1371/journal.pone.0163962

Tumescheit C, Firth AE, Brown K. CIAlign: A highly customisable command line tool to clean, interpret and visualise multiple sequence alignments. PeerJ. 2022;10: e12983. doi:10.7717/peerj.12983
