#  Reports
#  ------------


# SEQKIT, report on raw data
# NB this is report on sequences/*.fas not on processed samples
# --------------------------------------------------

rule seqkit_stats_initial:
    input:
        infolder = "resources/samples"
    output:
        "results/reporting/seqkit/initial_seqkit_report.md",
    shell:
        "seqkit stats -b {input.infolder}/*.fas | csvtk csv2md -t > {output}"


# AMAS, alignment report
# --------------------------------------------------

rule AMAS_alignment_stats:
    input:
        expand("results/trimal/{sample}_mafft_trimal.fas", sample=SAMPLES),
    output:
        "results/reporting/amas/{sample}_mafft_trimal_amas.tsv",
    shell:
        "python workflow/scripts/AMAS.py summary -i {input} -f fasta -d dna -o {output}"


# AMAS, alignment length plot
# --------------------------------------------------


rule alignlen_plot:
    input:
        "results/reporting/amas/2012_145_mafft_amas.tsv",
    output:
        "results/reporting/amas/2012_145_mafft_amas_alignlength.png",
    script:
        "../scripts/plot_stats.py"
