# Rules relating to alignments
# ------------------------------
# functions get_added_seqs and get_cialignment etc
# are defined in rules/common.smk

# add sample seqs to reference alignment
rule mafft_add_seqs:
    input:
        newseqs = get_added_seqs,
        ref = REF_ALIGNMENT,
        # ref = REFERENCE,
    output:
        newalignment = "results/mafft/{sample}_mafft.fas"
    shell:
        "mafft --add {input.newseqs} --reorder {input.ref} > {output.newalignment}"

 
# check that sequences were added to the reference alignment and exit if not
rule check_seqs_added:
    input:
        seqs_to_add=get_added_seqs,
        combined_alignment="results/mafft/{sample}_mafft.fas",
    params:
        # reflibrary = REFERENCE,
        reflibrary = REF_ALIGNMENT,
    output:
        log="results/reporting/mafft/{sample}_checkaddseqs_log.txt",
    script:
        "../scripts/check_added.py"


# check for sequences with duplicated names and remove sequence
rule remove_duplicate_names:
    input:
        "results/mafft/{sample}_mafft.fas",
    output:
        aln="results/mafft/{sample}_mafft_nodups.fas",
        duplist="results/mafft/{sample}_mafft_duplist.txt",
    shell:
        "seqkit rmdup -n {input} > {output.aln} -D {output.duplist}"


# remove aligned sequences if nucleotide count below threshold
# seqs to retain no matter the length can be set in config.yaml
rule CIAlign_remove_short_seqs:
    input:
        fasta="results/mafft/{sample}_mafft_nodups.fas"
    output:
        "results/cialign/{sample}_mafft_cialign_shortremoved_cleaned.fasta"
    params:
        minlen=config.get("cialign_minlen", 300),
        stem=lambda wc: f"results/cialign/{wc.sample}_mafft_cialign_shortremoved",
        retain=cialign_short_retain_arg()
    shell:
        """
        CIAlign \
            --infile {input.fasta} \
            --outfile_stem {params.stem} \
            --remove_short \
            --remove_min_length {params.minlen} \
            {params.retain}
        """


rule CIAlign_remove_divergent_trim:
    input:
        alignment = get_cialignment, # either shortseqs removed or not depending on config
    output:
        cleaned = "results/cialign/{sample}_mafft_cialign_cleaned.fasta",
        log     = "results/cialign/{sample}_mafft_cialign_log.txt",
        removed = "results/cialign/{sample}_mafft_cialign_removed.txt",
    params:
        stub = lambda wildcards, output: output.cleaned.replace("_cleaned.fasta", ""),
    shell:
        """
        CIAlign --infile {input.alignment} --outfile_stem {params.stub} --remove_divergent --crop_ends
        """


