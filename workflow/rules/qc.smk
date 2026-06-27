# remove problematic characters and whitespace, replace with underscores
# ie parenthesis, commas, square-brackets, colon, semi-colon, and whitespace
# remove -.? from sequences. Report to log file
rule clean_supplied_fasta:
    input:
        "resources/samples/{sample}.fas",
    output:
        seqs="results/samples/{sample}_validated.fas",
        log="results/reporting/validated/{sample}_clean_fasta_log.txt",
        names="results/reporting/validated/{sample}_all_fasta_headers.txt",
    message:
        "Validating and cleaning FASTA records for {wildcards.sample}"
    script:
        "../scripts/clean_fasta_txt.py"


# appends a unique number to each seq ID: >seq1 to >seq1_1
# rule fasta_number_headers:
#     input:
#         expand("results/qc/{sample}_minlength.fas", sample=SAMPLES),
#     output:
#         "results/qc/{sample}_numbered.fas",
#     shell:
#         'seqkit replace -p $ -r "_{nr}" {input} > {output}'

# enforce a minimum sequence length, specified in the config file
# rule minlength:
#     input:
#         expand("resources/samples/{sample}.fas", sample=SAMPLES),
#     output:
#         "results/qc/{sample}_minlength.fas",
#     params:
#         minlength = config["min_seq_length"],
#     shell:
#         "seqkit seq -m {params.minlength} -g {input} > {output}"
