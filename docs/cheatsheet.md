# conda snakemake cheatsheet

## Conda create & activate

```
conda env create --name snakemake-tutorial --file environment.yaml
```
if .yaml has name option specified
```
conda env create -f envs/environment.yaml
```
```
conda activate snakemake-tutorial
mamba env update -f workflow/envs/environment.yaml
conda info --envs
conda env export > environment_out.yml
conda install -c bioconda flash
conda config --set channel_priority strict
```

## Snakemake

```
snakemake --dag | dot -Tsvg > dag.svg
snakemake --dag results/final_fasta/*.fastq | dot -Tsvg > dag.svg
snakemake --rulegraph | dot -Tpng > results/rule-graph.png

snakemake -s testsnakefile.smk
snakemake --forceall
snakemake --delete-all-output -n
```

## VS Code

ctr-opt-cmd-P is show md preview in panel
