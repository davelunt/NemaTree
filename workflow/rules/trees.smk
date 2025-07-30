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

rule iqtree: # ML phylogenetic analysis
    input:
        expand("results/cialign/{sample}_mafft_cialign_cleaned.fasta", sample=SAMPLES),
    output:
        expand("results/iqtree/{sample}/{sample}_mafft_cialign_iqtree.treefile", sample=SAMPLES),
    params:
        model = config["subst_model"],
        dir = directory("results/iqtree/{sample}/"),
    shell:
        """
        iqtree -s {input} \
        -pre {params.dir} \
        -m {params.model} \
        --seqtype DNA \
        --quiet \
        -T AUTO \
        """
        # -redo \

# plot tree with toytree
# highlight tips that were added to the reference alignment
# ---------------------------------------------------------
rule toytree_plot:
    input:
        nwk = expand("results/iqtree/{sample}/{sample}_mafft_cialign_iqtree.treefile", sample=SAMPLES),
        added = expand("results/reporting/validated/{sample}_all_fasta_headers.txt", sample=SAMPLES),
    output:
        expand("results/toytree/{sample}_mafft_cialign_iqtree.html", sample=SAMPLES),
    script:
        "../scripts/toytre.py"
