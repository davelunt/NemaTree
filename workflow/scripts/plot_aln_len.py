# plot alignment statistics
# --------------------------------------------------
# use AMAS to write a report on alignments
# import into pandas
# plot histograms using seaborn

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# AMAS report, replace summary with {title}
# ALN_REPORT = pd.read_table("reports/amas/summary.tsv")
ALN_REPORT = pd.read_table(snakemake.input[0])

sns.set_style("whitegrid")

sns.histplot(ALN_REPORT, x="Alignment_length", bins=20, color="red", alpha=0.8)
plt.savefig(snakemake.output[0])

# sns.histplot(ALN_REPORT, x="Parsimony_informative_sites",
#              color='blue',
#              bins=20,
#              alpha=0.8)
# plt.savefig("results/plots/parsinformative_plot2.png")
