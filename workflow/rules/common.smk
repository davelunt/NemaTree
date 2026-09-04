
# Samples from config
SAMPLES = list(config["samples"].keys())

def get_raw_input(wildcards):
    """Retrieves the original raw user path for the initial rule."""
    return config["samples"][wildcards.sample]


def get_added_seqs(wildcards):
    """
    Evaluates files *already processed* inside results/ 
    ie downstream input function. Selects based on config file
    """
    if config.get("enforce_minlength", False):
        return f"results/samples/{wildcards.sample}_valid_minlen.fas"
    else:
        return f"results/samples/{wildcards.sample}_validated.fas"


# get correct reference alignment from config

VALID_LOCI = {"SSU", "LSU"}
VALID_SCOPES = {"genus", "clades123"}

def get_reference(config):
    """Resolve the reference alignment path from locus and scope choices."""
    locus = config["locus"]
    scope = config["scope"]

    if locus not in VALID_LOCI:
        raise ValueError(f"config 'locus' must be one of {sorted(VALID_LOCI)}, got '{locus}'")
    if scope not in VALID_SCOPES:
        raise ValueError(f"config 'scope' must be one of {sorted(VALID_SCOPES)}, got '{scope}'")

    return config["reference_alignments"][locus][scope]


def get_cialignment(wildcards):
    """
    Pass the current alignment, which can vary based on config
    """
    if config.get("cialign_len_filter", False):
        return f"results/cialign/{wildcards.sample}_mafft_cialign_shortremoved_cleaned.fasta"
    else:
        return f"results/mafft/{wildcards.sample}_mafft_nodups.fas" 


def cialign_short_retain_arg():
    """
    Pass the file of sequences to retain, irrespective of length, if 
    config retain_short_list_seqs: True
    """
    if config.get("retain_short_list_seqs", False):
        return f'--remove_short_retain_list "{config["cialign_retain_short_list"]}"'
    return ""