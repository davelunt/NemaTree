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


# appends a unique number to each seq ID: >seqA to >seqA_001
# rule fasta_number_headers:
#     input:
#         "results/samples/{sample}_validated.fas",
#     output:
#         "results/samples/{sample}_numbered.fas",
#     shell:
#         'seqkit replace -p $ -r "_{nr:03d}" {input} > {output}'

# enforce a minimum sequence length, of added sequences
# specified in the config file
rule minlength:
    input:
        "results/samples/{sample}_validated.fas",
    output:
        "results/samples/{sample}_minlength.fas",
    params:
        minlength = config["min_seq_length"],
    shell:
        "seqkit seq -m {params.minlength} -g {input} > {output}"
