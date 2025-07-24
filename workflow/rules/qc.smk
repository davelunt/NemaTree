rule minlength:
    input:
    output:
    params:
        minlength = config["min_seq_length"]
    shell:
        "seqkit seq -m {params.minlength} -g {input} > {output}"


rule fasta_number_headers:
    input:
    output:
    shell:
        'seqkit replace -p $ -r "_{nr}" {input} > {output}'
