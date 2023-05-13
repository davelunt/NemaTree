rule all:
    input:
        "results/mad/ape_COI.afa.treefile.rooted.nwk"

rule mad_root:
    input:
        "results/iqtree/ape_COI.afa.treefile"
    output:
        "results/mad/ape_COI.afa.treefile.rooted.nwk"
    shell:
        "python scripts/mad_root2.py {input} {output}"