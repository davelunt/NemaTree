
# exclude sequences from reference alignment
# rule seqkit_remove_seqs:
#     input:
#         excluded = config["exclusion_list_reference"],
#         ref = config["reference_alignment"],
#     output:
#         "resources/reference/18Sreference_new.fas",
#     shell:
#         "seqkit grep -v -n -f {input.excluded} {input.ref} > {output}"

# add sequences to the reference alignment
rule mafft_add_seqs:
    input:
        newseqs=expand("resources/samples/{sample}_validated.fas", sample=SAMPLES),
    output:
        newalignment=expand("results/mafft/{sample}_mafft.fas", sample=SAMPLES),
    params:
        ref=config["reference_alignment"],
    shell:
        "mafft --add {input.newseqs} --reorder {params.ref} > {output.newalignment}"


# mafft --add sequences can fail silently, this checks that the sequences were added
rule check_seqs_added:
    input:
        seqs_to_add="resources/samples/{sample}_validated.fas",
        combined_alignment="results/mafft/{sample}_mafft.fas",
    params:
        reflibrary=config["reference_alignment"],
    output:
        log="results/reporting/mafft/{sample}_checkaddseqs_log.txt",
    script:
        "../scripts/check_added.py"


# CIAlign alignment quality control
rule CIAlign_remove_divergent_trim:
    input:
        "results/mafft/{sample}_mafft.fas",
    output:
        "results/cialign/{sample}_mafft_cialign_cleaned.fasta",
    params:
        stub="results/cialign/{sample}_mafft_cialign",
    shell:
        """
        CIAlign --infile {input} --outfile_stem {params.stub} --remove_divergent --crop_ends
        """
