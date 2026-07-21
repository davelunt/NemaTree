#  Reports
#  ------------


# SEQKIT, report on initial fasta file
rule seq_stats_initial:
    input:
        valid="results/samples/{sample}_validated.fas",
    output:
        "results/reporting/seqkit/{sample}_initial_seqkit_report.md",
    shell:
        "seqkit stats -b {input.valid} | csvtk csv2md -t > {output}"


# plot sequence length histogram of fasta sequences added
rule plot_seq_len:
    input:
        "results/samples/{sample}_validated.fas",
    output:
        tsv="results/reporting/plots/{sample}_lengths.tsv",
        html="results/reporting/plots/{sample}_length_histogram.html",
        png="results/reporting/plots/{sample}_length_histogram.png",
    script:
        "../scripts/plot_lens.py"


# plot sequence length histogram of alignment seqs
rule plot_alnseq_len:
    input:
        "results/cialign/{sample}_mafft_cialign_cleaned.fasta",
    output:
        tsv="results/reporting/plots/{sample}_alnseqlengths.tsv",
        html="results/reporting/plots/{sample}_alnseqlength_histogram.html",
        png="results/reporting/plots/{sample}_alnseqlength_histogram.png",
    script:
        "../scripts/plot_lens.py"


# AMAS, alignment report
rule AMAS_alignment_stats:
    input:
        "results/cialign/{sample}_mafft_cialign_cleaned.fasta",
    output:
        "results/reporting/amas/{sample}_mafft_cialign_amas.tsv",
    shell:
        "python workflow/scripts/AMAS.py summary -i {input} -f fasta -d dna -o {output}"


# CIAlign, alignment reporting and visualisations
rule CIAlign_aln_statsvisuals:
    input:
        fasta = "results/cialign/{sample}_mafft_cialign_cleaned.fasta",
    output:
        img = "results/reporting/cialign/{sample}_mafft_cialign_output.png",
    params:
        stub = lambda wildcards, output: output.img.replace("_output.png", ""),
    shell:
        """
        CIAlign --infile {input.fasta} --outfile_stem {params.stub} --visualise --plot_stats_input
        """
