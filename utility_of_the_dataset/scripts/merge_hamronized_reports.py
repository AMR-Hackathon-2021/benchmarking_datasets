'''
Merge reports from hAMRonization_workflow
'''


import sys, os, glob,json, csv
import pandas as pd 

files = glob.glob(os.path.join("results/*/*","*"))
df_list = []

for f in files:
	if os.path.isfile(f) and "hamronized_report.tsv" in f:
		try:
			with open(f, 'r') as csvfile:
				df = pd.read_csv(f, sep="\t")
				df_list.append(df)
		except Exception as e:
			print("WARNING: file {}, {}".format(f,e))

all_dfs = pd.concat(df_list)

selected_columns_df = all_dfs[["input_file_name","gene_symbol","analysis_software_name"]]

selected_columns_df.to_csv("output.tsv",sep="\t", index=False)


