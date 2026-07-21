
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


def get_cialignment(wildcards):
    """
    Pass the current alignment, which can vary based on config
    """
    if config.get("cialign_len_filter", False):
        return f"results/cialign/{wildcards.sample}_mafft_cialign_shortremoved.fas"
    else:
        return f"results/mafft/{wildcards.sample}_mafft_nodups.fas" 
