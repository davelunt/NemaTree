# remove problematic characters and whitespace, replace with underscores
# ie parenthesis, commas, square-brackets, colon, semi-colon, and whitespace
# remove -.? from sequences. Report to log file
rule clean_supplied_fasta:
    input:
        # "resources/samples/{sample}.fas",
        raw = get_raw_input,
    output:
        seqs="results/samples/{sample}_validated.fas",
        log="results/reporting/validated/{sample}_clean_fasta_log.txt",
        names="results/reporting/validated/{sample}_all_fasta_headers.txt",
    message:
        "Validating and cleaning FASTA records for {wildcards.sample}"
    script:
        "../scripts/clean_fasta_txt.py"


# Conditional rule (only runs if enforce_minlength is True)
# excludes sequences less than config "min_seq_length"
rule minlength:
    input:
        "results/samples/{sample}_validated.fas",
    output:
        "results/samples/{sample}_valid_minlen.fas",
    params:
        minlength = config["min_seq_length"],
    shell:
        "seqkit seq -m {params.minlength} -g {input} > {output}"
