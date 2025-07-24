# rule align_format_convert:
#     input:
#         "resources/samples/2012_fig_fullname.fas",
#     output:
#         "resources/samples/2012_fig_fullname_cleanup.fas",
#     params:
#         informat="fasta",
#         outformat="fasta",
#     script:
#         "../scripts/aln_convert.py"

rule mafft_align:
    input:
        expand("resources/samples/{sample}.fas", sample=SAMPLES),
    output:
        "results/mafft/{sample}_mafft.fas",
    shell:
        "mafft --auto --quiet --reorder {input} > {output}"

rule mafft_add_seqs:
    input:
        newseqs = "resources/samples/{newseq}", newseq=config["sequences_to_add"],
        alignment = "results/alignments/{alignment}", alignment=config["alignment_to_add_to"],
    output:
        newalignment = "results/mafft/{newseq}_{alignment}.fas",
    shell:
        "mafft --add {input.newseqs} --reorder {input.alignment} > {output.newalignment}"

rule trimal: 
    input:
        expand("results/mafft/{sample}_mafft.fas", sample=SAMPLES),
    output:
        "results/trimal/{sample}_mafft_trimal.fas",
    shell:
        "trimal -in {input} -out {output} -gappyout -keepheader"


# if configfile specifies sequences to be removed, remove using seqkit
# if REMOVE-SEQS is 'TRUE':
#     rule remove_listed_seqs:
#         message: "Removing sequences specified by config file"
#         input:
#             alignment = "results/alignments/2012_154.fas",
#             exclusionlist = config["exclusion_list"],
#         output:
#             "results/alignments/pxrms/2012_147.fas"
#         shell:
#             "seqkit grep -n -v -f {input.exclusionlist} {input.alignment} > {output}"
# else print("No sequences were specified by the configfile to be excluded")

