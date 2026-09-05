# Phylogenetic analysis
# =====================

# IQtree, build ML tree
# ----------------------
rule iqtree:
    message:
        "Building ML tree with IQtree for sample {wildcards.sample}.fas"
    input:
        "results/cialign/{sample}_mafft_cialign_cleaned.fasta",
    output:
        treefile="results/iqtree/{sample}_mafft_cialign_cleaned_iqtree.treefile",
    params:
        # model=config["subst_model"],
        model=SUBST_MODEL,
        prefix="results/iqtree/{sample}_mafft_cialign_cleaned_iqtree",
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
        nwk="results/iqtree/{sample}_mafft_cialign_cleaned_iqtree.treefile",
        added="results/reporting/validated/{sample}_all_fasta_headers.txt",
    output:
        "results/reporting/toytree/{sample}_mafft_cialign_cleaned_iqtree.{ext}",
    script:
        "../scripts/toytree_colours.py"
