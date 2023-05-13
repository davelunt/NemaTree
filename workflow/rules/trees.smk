# Phylogenetic analysis
# =====================

# FastTree, build ML tree
# --------------------------------------------------

rule fasttree:
    input:
        "results/alignments/{sample}.fas"
    output:
        "results/fasttree/{sample}_fasttree.nwk"
    shell:
        "FastTree -quiet -gtr -nt {input} > {output}"


# IQtree, build ML tree
# --------------------------------------------------

rule iqtree: # ML phylogenetic analysis
    input:
        "results/alignments/{sample}.fas"
    output:
        "results/iqtree/{sample}_iqtree.treefile"
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
        "results/fasttree/{sample}_fasttree.nwk",
    output:
        "results/madroot/{sample}_fasttree_rooted.nwk"
    shell:
        "python scripts/mad_root2.py {input} {output}"

