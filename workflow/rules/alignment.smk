# Rules relating to alignments
# ------------------------------

# remove sequences from reference alignment according to exclusion list
from workflow.rules.common import get_added_seqs


rule filter_reference_alignment:
    input:
        ref_orig=get_ref_alignment,
        remove_list=config["exclusion_list"],
    output:
        new_ref=REF_FILTERED,
    shell:
        "seqkit grep -v -n -f {input.remove_list} {input.ref_orig} > {output.new_ref}"


# add sample sequences to the reference alignment
rule mafft_add_seqs:
    input:
        # newseqs="results/samples/{sample}_validated.fas",
        newseqs = get_added_seqs, # current validated and filtered sequences
        ref = get_ref_alignment, # current reference from common.smk rule
    output:
        newalignment="results/mafft/{sample}_mafft.fas",
    shell:
        "mafft --add {input.newseqs} --reorder {input.ref} > {output.newalignment}"

# check that sequences were added to the reference alignment and exit if not
rule check_seqs_added:
    input:
        seqs_to_add=get_added_seqs,
        combined_alignment="results/mafft/{sample}_mafft.fas",
    params:
        reflibrary = get_ref_alignment,
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

# rule CIAlign_remove_short_seqs:
#     input:
#         "results/mafft/{sample}_mafft_nodups.fas",
#     output:
#         "results/cialign/{sample}/{sample}_mafft_cialign_shortremoved.fasta",
#     params:
#         minlen = config.get("cialign_min_sequence_length", 700),
#         shortlist = config.get("cialign_short_sequence_retain_list", []),
#         stem = "results/cialign/{sample}/{sample}_mafft_cialign_shortremoved",
#     shell:
#         """
#         CIAlign --infile {input} \
#                 --remove_min_length {params.minlen} \
#                 --remove_short_retain_list {params.shortlist} \
#                 --outfile_stem {params.stem}
#         """

# CIAlign alignment quality control. Removes divergent sequences and trims the alignment ends
rule CIAlign_remove_divergent_trim:
    input:
        "results/mafft/{sample}_mafft_nodups.fas",
    output:
        "results/cialign/{sample}_mafft_cialign_cleaned.fasta",
    params:
        stub="results/cialign/{sample}_mafft_cialign",
    shell:
        """
        CIAlign --infile {input} --outfile_stem {params.stub} --remove_divergent --crop_ends
        """
