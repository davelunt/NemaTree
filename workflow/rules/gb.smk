# download, convert, and process GenBank files

rule download_genbank:
    input:
        accessions=config["accession_file"],
    output:
        "resources/gb/accn_download.gb",
    params:
        email=config["ncbi_email"],
    script:
        "scripts/gbfetch.py",

# convert gb to fasta, and write a tsv file with metadata
rule convert_gb_to_fasta:
    input:
        "resources/gb/accn_download.gb",
    output:
        fasta="resources/gb/accn_download.fas",
        tsv="resources/accn_download.tsv",
    script:
        "scripts/gb_parse_tsv.py",

rule minlength:
    input:
        "resources/gb/accn_download.fas",
    output:
        "resources/gb/accn_download_minlen.fas",
    params:
        minlength = config["min_seq_length"],
    shell:
        "seqkit seq -m {params.minlength} -g {input} > {output}"

# remove problematic characters and whitespace, replace with underscores
# ie parenthesis, commas, square-brackets, colon, semi-colon, and whitespace
rule sanitize_fasta_headers
    input:
        "resources/gb/accn_download_minlen.fas",
    output:
        "resources/samples/accn_download_minlen_clean.fas",
    script:
        "scripts/sanitize_fasta_headers.py",