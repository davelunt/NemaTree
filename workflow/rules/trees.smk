# Phylogenetic analysis
# =====================

# FastTree, build ML tree
# --------------------------------------------------

# rule fasttree:
#     input:
#         expand("results/mafft/{sample}_mafft.fas", sample=SAMPLES),
#     output:
#         expand("results/fasttree/{sample}_mafft_fasttree.nwk", sample=SAMPLES),
#     shell:
#         "FastTree -quiet -gtr -nt {input} > {output}"


# IQtree, build ML tree. May need to add --latency-wait SECONDS flag to snakemake command
# to allow for longer processing time.
# --------------------------------------------------


# ML phylogenetic analysis
rule iqtree:
    message:
        "Building ML tree with IQtree for sample {wildcards.sample}.fas"
    input:
        "results/cialign/{sample}_mafft_cialign_cleaned.fasta",
    output:
        treefile="results/iqtree/{sample}_mafft_cialign_iqtree.treefile",
    params:
        model=config["subst_model"],
        prefix="results/iqtree/{sample}_mafft_cialign_iqtree",
    shell:
        """
        iqtree -s {input} \
               -pre {params.prefix} \
               -m {params.model} \
               --seqtype DNA \
               -redo \
               --quiet \
               -T AUTO
        """


# plot tree with toytree
# highlight tips that were added to the reference alignment
# ---------------------------------------------------------
rule toytree_plot:
    input:
        nwk="results/iqtree/{sample}_mafft_cialign_iqtree.treefile",
        added="results/reporting/validated/{sample}_all_fasta_headers.txt",
    output:
        "results/reporting/toytree/{sample}_mafft_cialign_iqtree.{ext}",
    script:
        "../scripts/toytree_colours.py"
