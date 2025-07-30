#  Reports
#  ------------

# SEQKIT, report on initial fasta file
rule seqkit_stats_initial:
    input:
        infolder = "resources/samples"
    output:
        "results/reporting/seqkit/initial_seqkit_report.md",
    shell:
        "seqkit stats -b {input.infolder}/*.fas | csvtk csv2md -t > {output}"

# plot sequence length histogram of fasta sequences
rule plot_seq_len:
    input:
        expand("resources/samples/{sample}.fas", sample=SAMPLES),
    output:
        html = "results/reporting/plots/{sample}_length_histogram.html",
        png = "results/reporting/plots/{sample}_length_histogram.png",
    script:
        "scripts/plot_lens.py"

# AMAS, alignment report
rule AMAS_alignment_stats:
    input:
        expand("results/trimal/{sample}_mafft_trimal.fas", sample=SAMPLES),
    output:
        "results/reporting/amas/{sample}_mafft_trimal_amas.tsv",
    shell:
        "python workflow/scripts/AMAS.py summary -i {input} -f fasta -d dna -o {output}"

# CIAlign, alignment reporting and visualisations
rule CIAlign_visualise:
    input:
        expand("results/cialign/{sample}_mafft_cialign_cleaned.fasta", sample=SAMPLES),
    output:
        dir = directory("results/reporting/cialign/{sample}/"),
    shell:
        "CIAlign --infile {input} --outfile_stem {output} --visualise --plot_stats_input"

# plot alignment lengths from AMAS report
rule alignlen_plot:
    input:
        "results/reporting/amas/2012_145_mafft_amas.tsv",
    output:
        "results/reporting/amas/2012_145_mafft_amas_alignlength.png",
    script:
        "scripts/plot_aln_len.py"
