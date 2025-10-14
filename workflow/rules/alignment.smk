# Rules relating to alignments

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
        newseqs="resources/samples/{sample}_validated.fas",
    output:
        newalignment="results/mafft/{sample}_mafft.fas",
    params:
        ref=f"resources/reference/{config['reference_alignment']}.fas",
    conda:
        "envs/environment.yaml",
    shell:
        "mafft --add {input.newseqs} --reorder {params.ref} > {output.newalignment}"


# mafft --add sequences can fail silently, this checks that the sequences were added
rule check_seqs_added:
    input:
        seqs_to_add="resources/samples/{sample}_validated.fas",
        combined_alignment="results/mafft/{sample}_mafft.fas",
    params:
        reflibrary=f"resources/reference/{config['reference_alignment']}.fas",
    output:
        log="results/reporting/mafft/{sample}_checkaddseqs_log.txt",
    conda:
        "envs/environment.yaml",
    script:
        "../scripts/check_added.py"


# check for sequences with duplicated names and remove sequence
rule remove_duplicate_names:
    input:
        "results/mafft/{sample}_mafft.fas",
    output:
        aln="results/mafft/{sample}_mafft_nodups.fas",
        duplist="results/mafft/{sample}_mafft_duplist.txt",
    conda:
        "envs/environment.yaml",
    shell:
        "seqkit rmdup -n {input} > {output.aln} -D {output.duplist}"


# CIAlign alignment quality control
rule CIAlign_remove_divergent_trim:
    input:
        "results/mafft/{sample}_mafft_nodups.fas",
    output:
        "results/cialign/{sample}_mafft_cialign_cleaned.fasta",
    params:
        stub="results/cialign/{sample}_mafft_cialign",
    conda:
        "envs/environment.yaml",
    shell:
        """
        CIAlign --infile {input} --outfile_stem {params.stub} --remove_divergent --crop_ends
        """
