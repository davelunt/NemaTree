rule align_format_convert:
    input:
        "resources/samples/2012_fig_fullname.fas",
    output:
        "resources/samples/2012_fig_fullname_dna_cleanup.fas",
    params:
        informat="fasta",
        outformat="fasta",
    script:
        "../scripts/aln_convert.py"