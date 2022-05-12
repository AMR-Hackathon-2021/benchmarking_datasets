#### Comparing AMR tools

We compared AMR tools before choosing one to produce the benchmarking datasets.
We used the hAMRonization workflow (https://github.com/pha4ge/hAMRonization) for this task. The hAMRonization workflow uses 12 different AMR tools to predict AMR genes in genomic data and produces a standard report to compare results across the tools.

#### Data

We analysed 94 assembled genomes downloaded from NCBI.

#### Analysis

1. Generate data for radar plot using the following:

```
python3 scripts/radar_plot_data.py > analysis/radar_data_94_samples.tsv
```

2. Generate data for sankey plot using the following:

```
python3 scripts/merge_hamronized_reports.py
```


#### Results (in analysis directory)

- radar_data_94_samples.tsv
- sankey_data_94_samples.tsv

