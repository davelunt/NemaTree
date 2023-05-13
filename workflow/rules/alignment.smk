REMOVE-SEQS = "config["exclude_seqs"]"

rule align_format_convert:
    input:
        "resources/samples/2012_fig_fullname.fas",
    output:
        "resources/samples/2012_fig_fullname_cleanup.fas",
    params:
        informat="fasta",
        outformat="fasta",
    script:
        "../scripts/aln_convert.py"

# if configfile specifies sequences to be removed, remove using seqkit
if REMOVE-SEQS == 'TRUE':
    rule remove_listed_seqs:
        message: "Removing sequences specified by config file"
        input:
            alignment = "results/alignments/2012_154.fas",
            exclusionlist = config["exclusion_list"],
        output:
            "results/alignments/pxrms/2012_147.fas"
        shell:
            "seqkit grep -n -v -f {input.exclusionlist} {input.alignment} > {output}"
else print("No sequences were specified by the configfile to be excluded")


rule mafft_add_seqs:
    input:
        newseqs = "resources/samples/newsequences.fas",
        alignment = "results/alignments/2012_154.fas",
    output:
        "results/mafft/2012_154_addedseqs.fas"
    shell:
        "mafft --add {input.newseqs} --reorder {input.alignment} > {output}"
