# List of output files

This is an overview of the files written by the workflow
`sample` at the start of each name is text defined in config/config.yaml as the name given to your input fasta file

The results files below are alphabetical not in order of being processed

Some output is created or not depending on your config settings

The final treefile you will want to look at is `reporting/toytree/sample_mafft_cialign_cleaned_iqtree.html`

results/
    cialign/
        sample_mafft_cialign_cleaned.fasta # alignment file after processing
        sample_mafft_cialign_log.txt # log file written by cialign
        sample_mafft_cialign_removed.txt # list of sequences removed
        # if minlen filter is applied in config
        sample_mafft_cialign_shortremoved_cleaned.fasta # alignment file after processing
        sample_mafft_cialign_shortremoved_log.txt # log file written by cialign
        sample_mafft_cialign_shortremoved_removed.txt # list of sequences removed
    iqtree/
        sample_mafft_cialign_cleaned_iqtree.bionj
        sample_mafft_cialign_cleaned_iqtree.ckp.gz
        sample_mafft_cialign_cleaned_iqtree.iqtree
        sample_mafft_cialign_cleaned_iqtree.log
        sample_mafft_cialign_cleaned_iqtree.mldist
        sample_mafft_cialign_cleaned_iqtree.treefile
        sample_mafft_cialign_cleaned_iqtree.uniqueseq.phy
    mafft/
        sample_mafft_duplist.txt
        sample_mafft_nodups.fas
        sample_mafft.fas
    reporting/
        amas/
            sample_mafft_cialign_amas.tsv
        cialign/
            # if plot printing is enabled
            sample_mafft_cialign_cleaned.fasta
            sample_mafft_cialign_input_changefreq.png
            sample_mafft_cialign_input_column_stats.tsv
            sample_mafft_cialign_input_coverage.png
            sample_mafft_cialign_input_information_content.png
            sample_mafft_cialign_input_resfreq.png
            sample_mafft_cialign_input_shannon_entropy.png
            sample_mafft_cialign_input.png
            sample_mafft_cialign_log.txt
            sample_mafft_cialign_markup_legend.png
            sample_mafft_cialign_markup.png
            sample_mafft_cialign_output.png
            sample_mafft_cialign_removed.txt
        mafft/
            sample_checkaddseqs_log.txt
        ?plots/
            sample_length_histogram.html
            sample_length_histogram.png
            sample_lengths.tsv
        ?seqkit/
            initial_seqkit_report.md
        text/
        toytree/
            sample_mafft_cialign_cleaned_iqtree.html
        validated/
            sample_all_fasta_headers.txt
            sample_clean_fasta_log.txt
    samples/
        sample_validated.fas
    