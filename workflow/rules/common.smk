def get_added_seqs(wildcards):
    return (
        f"results/samples/{wildcards.sample}_minlength.fas"
        if config.get("enforce_minlength", False)
        else f"results/samples/{wildcards.sample}_validated.fas"
    )
