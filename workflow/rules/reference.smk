# IQtree, build ML tree of reference sequences. 
# May need to add --latency-wait SECONDS flag to snakemake command
# to allow for longer processing time.
# --------------------------------------------------
# REF = config["reference_alignment"]

# ML phylogenetic analysis
rule iqtree:
    input:
        # ref = config["reference_alignment"],
        "resources/reference/{refalign}.fas", # refalign=REF
    output:
        treefile = "results/reference/{refalign}_iqtree.treefile",
    params:
        model = config["subst_model"],
        prefix = "results/reference/{refalign}_iqtree",
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
#         mkdir -p results/iqtree/{wildcards.sample}


# plot tree with toytree
# highlight tips that were added to the reference alignment
# ---------------------------------------------------------
rule toytree_plot:
    input:
        nwk = "results/reference/{refalign}_iqtree.treefile",
    output:
        "results/reference/{refalign}_iqtree.html",
    script:
        "../scripts/toytreref.py"
