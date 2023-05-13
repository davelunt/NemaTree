#  Reports
#  ------------


# SEQKIT, report on raw data
# NB this is report on sequences/*.fas not on processed samples
# --------------------------------------------------


rule seqkit_stats:
    input:
        infolder = "resources/sequences"
    output:
        "results/tables/seqkit/sequences_initial_seqkit_report",
    shell:
        "seqkit stats -b {input.infolder}/*.fas > {output}"


# AMAS, alignment report
# --------------------------------------------------


rule AMAS_alignment_stats:
    input:
        "results/biopythoncodons/{sample}_codons.fas",
    output:
        "results/tables/amas/{sample}_codons.fas.amas.tsv",
    shell:
        "AMAS.py summary -i {input} -f fasta -d dna -o {output} -c {threads}"


# AMAS, codon alignment length plot
# --------------------------------------------------


rule codon_alignlen_plot:
    input:
        "results/tables/amas/{sample}_codons.fas.amas.tsv",
    output:
        "results/plots/amas/{sample}_codon_alignlength.png",
    script:
        "../scripts/plot_stats.py"
