'''
Generate data in this format for all the amr tools in hAMRonization_workflow
gene	rgi	resfinder	csstar
A	1	1 	0
B	1	0	1
D	1	1	1

# use as test case SAMN02934530

'''

import sys, os, glob,json, csv

files = glob.glob(os.path.join("results/*/*","*"))

all_genes = [] # list

rgi = []
abricate =  []
csstar =  []
resfinder =  []
srax =  []

results = {}

def check_gene_in_list(l, g):
	if g in l:
		return 1
	else:
		return 0

for f in files:
	if os.path.isfile(f) and "hamronized_report.tsv" in f:
		with open(f, 'r') as csvfile:
			reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
			for row in reader:
				if(row[0] != "input_file_name"):
					print(row)
					exit
					if row[1] not in all_genes:
						all_genes.append(row[1])
					if "rgi" in row[6]:
						rgi.append(row[1])
					if "resfinder.py" in row[6]:
						resfinder.append(row[1])
					if "abricate" in row[6]:
						abricate.append(row[1])
					if "csstar" in row[6]:
						csstar.append(row[1])
					if "srax" in row[6]:
						srax.append(row[1])

print("Genes\tRGI\tresfinder\tabricate\tcsstar\tsrax")
for g in all_genes:
	print("{}\t{}\t{}\t{}\t{}\t{}".format(g,\
		check_gene_in_list(rgi, g),
		check_gene_in_list(resfinder, g),
		check_gene_in_list(abricate, g),
		check_gene_in_list(csstar, g),
		check_gene_in_list(srax, g),
		)
	)

