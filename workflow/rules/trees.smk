# Phylogenetic analysis
# =====================

# FastTree, build ML tree
# --------------------------------------------------

rule fasttree:
    input:
        expand("results/trimal/{sample}_mafft_trimal.fas", sample=SAMPLES),
    output:
        "results/fasttree/{sample}_mafft_trimal_fasttree.nwk",
    shell:
        "FastTree -quiet -gtr -nt {input} > {output}"


# IQtree, build ML tree
# --------------------------------------------------

rule iqtree: # ML phylogenetic analysis
    input:
        expand("results/trimal/{sample}_mafft_trimal.fas", sample=SAMPLES),
    output:
        "results/iqtree/{sample}_mafft_trimal_iqtree.treefile",
    shell:
        """
        iqtree -s {input} \
        -pre {output} \
        -m GTR+I+G \
        -quiet \
        -T AUTO \
        -redo \
        """

# Root the tree with MAD
# issues with passing files from multiple locations and saving output
# --------------------------------------------------
rule mad_root:
    input:
        "results/fasttree/2012_145_mafft_fasttree.nwk",
    output:
        "results/madroot/2012_145_mafft_fasttree_MADroot.nwk"
    shell:
        "python workflow/scripts/mad_root2.py {input} {output}"

#plot tree with toytree
# --------------------------------------------------
rule toytree_plot:
    input:
        expand("results/fasttree/{sample}_mafft_trimal_fasttree.nwk", sample=SAMPLES)
    output:
        "results/reporting/toytree/{sample}_mafft_trimal_fasttree_MAD.html",
    script:
        "../scripts/toytre.py"
