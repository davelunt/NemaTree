# Phylogenetic analysis
# =====================

# FastTree, build ML tree
# --------------------------------------------------

rule fasttree:
    input:
        expand("results/mafft/{sample}_mafft.fas", sample=SAMPLES),
    output:
        "results/fasttree/{sample}_mafft_fasttree.nwk",
    shell:
        "FastTree -quiet -gtr -nt {input} > {output}"


# IQtree, build ML tree. May need to add --latency-wait SECONDS flag to snakemake command
# to allow for longer processing time.
# --------------------------------------------------

rule iqtree: # ML phylogenetic analysis
    input:
        expand("results/mafft/{sample}_mafft.fas", sample=SAMPLES),
    output:
        dir = directory("results/iqtree/{sample}/"),
    params:
        model = config["subst_model"],
    shell:
        """
        iqtree -s {input} \
        -pre {output.dir} \
        -m {params.model} \
        --seqtype DNA \
        --quiet \
        -T AUTO \
        """
        # -redo \

#plot tree with toytree
# --------------------------------------------------
rule toytree_plot:
    input:
        nwk = expand("results/iqtree/{sample}/{sample}.treefile", sample=SAMPLES),
        added = "resources/validated/{sample}_all_fasta_headers.txt",
    output:
        "results/reporting/toytree/{sample}_mafft_iqtree.html",
    script:
        "../scripts/toytre.py"
