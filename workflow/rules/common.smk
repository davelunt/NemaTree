# from pathlib import Path

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


# def get_added_seqs(wildcards):
#     return (
#         f"results/samples/{wildcards.sample}_minlength.fas"
#         if config.get("enforce_minlength", False)
#         else f"results/samples/{wildcards.sample}_validated.fas"
#     )
