# Misc Notes

I'm putting things here until they find a better place.

## Why did you make this?

I've seen a lot of papers showing the distinctiveness of a new species, or regional sample, by comparison to only a very small number of other species isolates. I thought having publicly available well-curated reference alignments of Meloidogyne LSU and SSU would be very useful for this sort of research.

I'm a big believer in reproducibilty in data analysis as (a) its the right way to do science and (b) its the easiest way to do science. So I wrote a reproducible workflow to do Meloidogyne phylogenetic analysis. Using this workflow has saved me an enormous amount of time while automating best practice approaches.


## Minimum sequence length

Even though it reduces the number of taxa included, my view is that the phylogeny is much more robust if SSU sequences are required to be at least 700bp (config file).

```yaml
# CIAlign
cialign_len_filter: True # Filter short sequences from alignment
cialign_minlen: 700 # minimum sequence length (bp)
```

## My favourite species isn't separated phylogenetically

This does NOT mean your favourite taxon isn't a real taxonomic group. Many closely related species just do not separate with rRNA as there isn't enough information in the sequences. mtDNA isn't much better either. For closely related species genomics is the best approach as it has an enormous amount of data and isn't as hard as you might think.


## Excluded taxa due to taxonomic uncertainty


### M. oryzae

Some publications describe this in clade 3, while others have suggested that this species has been misidentified and falls into clade 1. This is discussed by Álvarez-Ortega et al (2019). ITS1 sequences place it in clade 1, while 18S sequences cannot distinguish it from M.graminicola in clade 3. Due to this confusion I do not include this species in the reference alignment. Many new full-length 18S sequences from well-characterised isolates (plus genomes) would resolve this more strongly.

Álvarez-Ortega S, Brito JA, Subbotin SA. Multigene phylogeny of root-knot nematodes and molecular characterization of Meloidogyne nataliei Golden, Rose & Bird, 1981 (Nematoda: Tylenchida). Sci Rep. 2019;9: 11788. doi:10.1038/s41598-019-48195-0


### M. christiae

Meloidogyne christiae KR082316 is the single SSU sequence from this taxon. It has a long branch in the 18S tree, making it subject to phylogenetic artefacts. Aisu et al (2026) have both SSU and LSU trees including M. christiae, though it falls in different taxonomic positions in each. This suggests that its taxonomic position is not reliable and many new full-length 18S sequences from well-characterised isolates (plus genomes) would resolve this more strongly.

Aisu J, Karssen G, De Oliveira DAS. Integrative taxonomy and mitogenome characterization of the root-knot nematode Meloidogyne silvestris. Sci Rep. 2026;16. doi:10.1038/s41598-026-54669-9


### M. duytsi

There are two SSU sequences of M. duytsi available from the international sequence databases (AF442197, KJ636385), the first falling very close to M.silvestris and the second elsewhere in the tree very close to M.dunensis. These are removed from the reference alignment as they do not add any clarity. You may of course add them yourself from these accession numbers. Again, many new full-length 18S sequences from well-characterised isolates (plus genomes) could resolve this.


## Why use only LSU and SSU? Why not add ? or merge both?

There is no reason at all, except that I had to start somewhere. This workflow could be modified to work with sequences of any locus, it would only require a good reference alignment (and some record keeping to clarify what type of sequences were being analysed). I have provided LSU and SSU reference alignments as they are probably the most commonly used. One issue with merging is that for most isolates since we do not know which 18S goes with which 26S sequence we would be creating synthetic sequences if we merged them. I see this a lot in publications where they restrict themselves to one representative of each species (a valid phylogenetic approach) but experience tells me that reducing taxon sampling like this is often problemmatic.


## Why not use genomes?

If you know me at all you will know that I just shouted "Yes!!" very loudly. This is the gold standard, and would reveal much more than simple taxonomy. To me the best phylogeny of the Meloidogyne tropical apomicts was figure 3 in Szitenberg et al 2017. This showed (against my expectations) that genome scale data could robustly resolve even the most closely related species with hybridization and polyploidy in their histories. It included many isolates of single species, but did not include a good sample of the genus.

Pushing this forward will require a community effort to grow well-characterised reference isolates for the genomics of species. I am of course happy to collaborate with anyone who needs bioinformatics support in their genomics projects.


## References

Szitenberg et al. Comparative Genomics of Apomictic Root-Knot Nematodes: Hybridization, Ploidy, and Dynamic Genome Change. Genome Biol. Evol. 2017. 2844–2861. doi:10.1093/gbe/evx201
