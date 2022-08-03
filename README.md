# Snakemake workflow: RKN-rRNA

[![Snakemake](https://img.shields.io/badge/snakemake-≥6.3.0-brightgreen.svg)](https://snakemake.github.io)
[![GitHub actions status](https://github.com/davelunt/RKN-rRNA/workflows/Tests/badge.svg?branch=main)](https://github.com/davelunt/RKN-rRNA/actions?query=branch%3Amain+workflow%3ATests)


A Snakemake workflow for analysis of root-knot nematode rRNA sequences

We use the structural alignments of SSU and LSU rRNA taken from SILVA. Long PCR products (~3kb) are then used to identify root-knot nematode individuals to species.

These analyses run as a snakemake workflow to ensure ease and reproducibility.

## Usage

The usage of this workflow is described in the [Snakemake Workflow Catalog](https://snakemake.github.io/snakemake-workflow-catalog/?usage=davelunt%2FRKN-rRNA).

If you use this workflow in a paper, don't forget to give credits to the authors by citing the URL of this (original) <repo>sitory and its DOI (see above).

# TODO

* Replace `<owner>` and `<repo>` everywhere in the template (also under .github/workflows) with the correct `<repo>` name and owning user or organization.
* The workflow will occur in the snakemake-workflow-catalog once it has been made public. Then the link under "Usage" will point to the usage instructions if `<owner>` and `<repo>` were correctly set.