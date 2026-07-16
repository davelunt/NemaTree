
# Samples from config
SAMPLES = list(config["samples"].keys())

def get_raw_input(wildcards):
    """Retrieves the original raw user path for the initial rule."""
    return config["samples"][wildcards.sample]


def get_added_seqs(wildcards):
    """
    Downstream input function. Evaluates files *already processed* inside results/.
    Selects either _valid_minlen or _validated based on configuration.
    """
    if config.get("enforce_minlength", False):
        return f"results/samples/{wildcards.sample}_valid_minlen.fas"
    else:
        return f"results/samples/{wildcards.sample}_validated.fas"


def get_cialignment(wildcards):
    """
    Pass the current alignment, which can vary based on config
    """
    if config.get("cialign_len_filter", False):
        return f"results/cialign/{wildcards.sample}_mafft_cialign_shortremoved.fas"
    else:
        return f"results/mafft/{wildcards.sample}_mafft_nodups.fas" 

# 
# get path stub to save report output from CIAlign. Parsed from output file
# used in rule reports.smk:CIAlign_aln_statsvisuals
# def get_cialign_reportstub(wildcards, output):
#     # Removes '_output.png' suffix to get the base stem
#     return str(output[0]).replace("_output.png", "")

# # used in rule alignment.smk: CIAlign_remove_divergent_trim
# def get_cialign_stub(wildcards, output):
#     # Removes '_cleaned.fasta' suffix to get the base stem
#     return str(output.cleaned).replace("_cleaned.fasta", "")