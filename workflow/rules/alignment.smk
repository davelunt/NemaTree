# Rules relating to alignments

# Only build filtered file if remove_seqs=True
rule filter_reference_alignment:
    input:
        ref_orig=REF_ORIGINAL
    output:
        new_ref=REF_FILTERED
    params:
        remove_list=config.get("exclusion_list_reference", [])
    shell:
        "seqkit grep -v -n -f {params.remove_list} {input.ref_orig} > {output.new_ref}"


# add sample sequences to the reference alignment
rule mafft_add_seqs:
    input:
        newseqs="results/samples/{sample}_validated.fas",
    output:
        newalignment="results/mafft/{sample}_mafft.fas",
    params:
        ref = get_ref_alignment, # current reference
    conda:
        "envs/environment.yaml",
    shell:
        "mafft --add {input.newseqs} --reorder {params.ref} > {output.newalignment}"


# rule mafft_add_seqs can fail silently, this checks that the sequences were added
rule check_seqs_added:
    input:
        seqs_to_add="results/samples/{sample}_validated.fas",
        combined_alignment="results/mafft/{sample}_mafft.fas",
    params:
        # reflibrary=f"resources/reference/{config['reference_alignment']}.fas",
        reflibrary = get_ref_alignment,
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

rule CIAlign_remove_short_seqs:
    input:
        "results/mafft/{sample}_mafft_nodups.fas",
    output:
        "results/cialign/{sample}/{sample}_mafft_cialign_shortremoved.fasta",
    params:
        minlen = config.get("cialign_min_sequence_length", 700),
        shortlist = config.get("cialign_short_sequence_retain_list", []),
        stem = "results/cialign/{sample}/{sample}_mafft_cialign_shortremoved",
    conda:
        "envs/environment.yaml",
    shell:
        """
        CIAlign --infile {input} \
                --remove_min_length {params.minlen} \
                --remove_short_retain_list {params.shortlist} \
                --outfile_stem {params.stem}
        """

# CIAlign alignment quality control. Removes divergent sequences and trims the alignment ends
rule CIAlign_remove_divergent_trim:
    input:
        "results/cialign/{sample}/{sample}_mafft_cialign_shortremoved.fasta",
    output:
        "results/cialign/{sample}/{sample}_mafft_cialign_cleaned.fasta",
    params:
        stub="results/cialign/{sample}/{sample}_mafft_cialign",
    conda:
        "envs/environment.yaml",
    shell:
        """
        CIAlign --infile {input} --outfile_stem {params.stub} --remove_divergent --crop_ends
        """
