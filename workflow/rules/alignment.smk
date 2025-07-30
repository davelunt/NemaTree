rule mafft_align:
    input:
        expand("resources/samples/{sample}.fas", sample=SAMPLES),
    output:
        "results/mafft/{sample}_mafft.fas",
    shell:
        "mafft --auto --quiet --reorder {input} > {output}"

# exclude sequences from reference alignment
# rule seqkit_remove_seqs:
#     input:
#         excluded = config["exclusion_list_reference"],
#         ref = config["reference_alignment"],
#     output:
#         "resources/reference/18Sreference_new.fas",
#     shell:
#         "seqkit grep -v -n -f {input.excluded} {input.ref} > {output}"

# this fails silently
rule mafft_add_seqs:
    input:
        newseqs = expand("resources/samples/validated/{sample}.fas", sample=SAMPLES)
        ref = config["reference_alignment"],
    output:
        newalignment = expand("results/mafft/{sample}_mafft.fas"),
    shell: 
        "mafft --add {input.newseqs} --reorder {input.ref} > {output.newalignment}"

# CIAlign CHECK THIS - DIRECTORY
    rule CIAlign_remove_divergent_trim:
        input:
            expand("results/mafft/{sample}_mafft.fas", sample=SAMPLES),
        output:
            dir = directory("results/cialign/{sample}_mafft_cialign"),
        shell:
            "CIAlign --infile {input} --outfile_stem {output.dir} --remove_divergent --crop_ends"


# rule trimal: 
#     input:
#         expand("results/mafft/{sample}_seqsadded_mafft.fas", sample=SAMPLES),
#     output:
#         "results/trimal/{sample}_seqsadded_mafft_trimal.fas",
#     shell:
#         "trimal -in {input} -out {output} -gappyout -keepheader"


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
