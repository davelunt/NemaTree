# Phylogenetic analysis of Root-Knot Nematode 18S rRNA sequences

This reproducible workflow processes 18S rRNA sequences from Root-Knot Nematodes, including quality control, alignment, and reporting. The workflow makes use of an alignment of sequences from the diversity of Meloidogyne species.

## Quickstart - for people used to this sort of thing

1. git clone the repo and create conda environment from `envs/environment.yaml`
2. add sequences to `resources/samples/myseqsname.fas`
3. add `myseqsname` to `config/config.yaml` as `seqs_to_add:`
4. final tree: `results/reporting/toytree/myseqsname_mafft_cialign_iqtree.html`

## Workflow Overview

The user should provide fasta sequences in a file in the `resources/samples/` directory with the `.fas` file extension.

The workflow can be configured using the `config.yaml` file, where you can specify parameters such as the minimum sequence length and the reference alignment file.

The workflow will:

1. Perform quality control on the sequences
2. Align the sequences to the reference alignment
4. Build a maximum likelihood tree
5. Generate a tree image as an html file

## Set up the workflow

1. download the workflow from GitHub
    - try: `git clone https://github.com/davelunt/RKN-RRNA.git`
2. prepare the software environment using `mamba` or `conda` and the `environment.yaml` file
    - install `mamba` and `conda` if you don't have them already
    - try `mamba env create -f envs/environment.yaml`

You should have miniconda installed. See instructions at the website https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html and install `mamba` with `conda install conda-forge::mamba`

Installing and using mamba may greatly increase the speed of creating the environment and is highly recommended. Although possibly slow the first time, creating this environment only needs to be done once per machine, not each time the workflow is run.

## Running the workflow

### Provide a single sequence file with .fas extension

Make sure you have provided (DNA not RNA) fasta sequences in a file in the `resources/samples/` directory with the `.fas` file extension. Using an informative short filename will help you keep track of your samples as it will be used throughout the workflow. No spaces in filenames. Do not provide multiuple files, place all fasta records in one fasta file. 

Tip: At a terminal in the workflow directory, run: `cat resources/samples/*.fas > resources/samples/myseqsname.fas` to combine all fasta files into one file.

### Check `config/config.yaml`

This file should contain:

- the basename of your `.fas` file containing your samples, e.g. myseqsname (REQUIRED)
- the basename of the reference alignment file to which your sequences will be aligned. Choose between the whole genus or just clades123 (OPTIONAL)

Except for the name of your sample file, all other config parameters have default values and can be left as is. You can also check `docs/tree_formatting.md` for more information on getting the best tree.

### Dry run, then run the workflow

Begin with a dry run to check setup and that all files are present.

`snakemake -np`

If all is well, run the workflow with:

`snakemake --cores 4 --latency-wait 300`

### Common problems

    - using .fasta not .fas
    - wrong capitalisation of the samples file name
    - spaces in filename, use_underscore_instead
    - wrong location (must be in `/resources/samples/`)
    - failure to install the environment with conda/mamba
        - try `mamba env create -f envs/environment.yaml`
    - failure to activate the environment
        - try `conda activate rkn-rrna`
    - snakemake times out waiting for IQ-tree after 30s. Use `--latency-wait 300`
    - losing the final tree
        - try `results/reporting/toytree/myseqsname_mafft_cialign_iqtree.html`
