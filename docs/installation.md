# Installation

This document gives extra help on installation and running the workflow.

Although the installation and set up has been carefully thought through, using best-practice approaches, this is always a challenge. No amount of help documentation for a programme like this can help you in all situations. Some of the problems you may encounter will require investigation on your own. Sorry.

## rationale

- The workflow is available by a simple `git clone` command
- The `conda` package manager is used to install the required software, and their dependencies
- `conda` is slow, so install `mamba` and use that instead/alongside `conda`

The first two sections, git and conda/mamba are the most difficult but only have to be done once. This works well on macOS and Linux. Windows is not well tested but may run on Windows Subsystem for Linux fine.

## git

- The workflow is hosted on github.com/davelunt/RKN-RRNA
- You can click the download button or use `git clone https://github.com/davelunt/NemaTree.git` at the command line

## conda and mamba package managers

You need to have miniconda installed. See instructions at the [conda website](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). NB this is miniconda not Anaconda (which is huge).

Install `mamba` with `conda install conda-forge::mamba`

Prepare the software environment using `mamba` and the `workflow/envs/environment.yaml` file. Try:

`mamba env create -f workflow/envs/environment.yaml`

This should install all the software as described in the environment.yaml file. At teh command line you should make sure that this environment is activated with `conda activate rkn-rrna`

Installing and using `mamba` instead of `conda` will greatly increase the speed of creating the environment and is highly recommended. Although possibly slow the first time, creating this environment only needs to be done once per machine, not each time the workflow is run.

## Testing and running the workflow

### Check `config/config.yaml`

This file is the only one you should have to touch. Everything can be configured using this simple text file.

Most things have sensible defaults, but you must specify the name of your sample file to analyse. See [sequence help doc](docs/sequence_prep.md)

### Dry run, then run the workflow

Begin with a dry run to check setup and that all files are present.

`snakemake -np`

If you do not get lots of red text clearly identifying problems all is probably good. If you do then have a look at the "Common Problems" sections (it is probably something simple. Otherwise I find Google AI is often good at interpreting the error messages.

Try to run the workflow with:

`snakemake --cores 4 --latency-wait 300`

If you do not get lots of angry red error text then it will run, reporting what it is doing, until the prompt reappears and it is finished. This takes 1-2 minutes on my M2 MacBook Air from 2023 with a small number of sequences. 

The final tree is at `results/reporting/toytree/myseqsname_mafft_cialign_cleaned_iqtree.html` (where myseqsname is the name of your sample file). You can open this in a web browser to view the tree.

If you want to have .png, .svg or .pdf trees this can be configured in the config file. You won't have to re-do the whole analysis, snakemake will just redo the tree graphics files using the treefile that was already generated.

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
        - try `results/reporting/toytree/myseqsname_mafft_cialign_cleaned_iqtree.html`

## Help docs

The documentation in `docs/` contains some more extensive help and advice:

- [installation](docs/installation.md): Information on installing the workflow and dependencies
- [sequence_prep](docs/sequence_prep.md): Information on preparing sequences to add
- [alignments](docs/alignments.md): Information on how sequence alignments are processed
- [tree_formatting](docs/tree_formatting.md): Information on tree formatting and rooting
