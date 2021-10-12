import argparse, sys, os, json, csv
# conda install dask or pip install dask
from dask import dataframe as dd

def main(args):
    all = []
    data = {}
    j = {}
    try:
        with open(os.path.join(args.accession_json), 'r') as jfile:
            j = json.load(jfile)
    except Exception as e:
        print(e)
        exit()

    for i in j["assemblies"]:
        data["assembly"] = i["assembly"]["assembly_accession"]
        print("assembly: {} ...".format(i["assembly"]["assembly_accession"]))
        for k in i["assembly"]["chromosomes"]:
            (terms, criteria) = get_prevalence_data_dask(args.prevalence_index, k["accession_version"])
            data["ncbi_accession"] = k["accession_version"]
            data["aro_terms"] = "; ".join(terms)
            data["rgi_criteria"] = "; ".join(criteria)
        all.append(data)
        print(json.dumps(all,indent=2))
    write_output(args.output_file, all)
    # print(json.dumps(data,indent=2))
    print("Done.")

def write_output(output_file, data):
    """
    Write output file to tabular
    """
    with open(output_file, "w") as tab_out:
        writer = csv.writer(tab_out, delimiter='\t', dialect='excel')
        writer.writerow(["assembly","ncbi_accession","aro_terms","rgi_criteria"])
        for i in data:
            writer.writerow([i["assembly"], i["ncbi_accession"], i["aro_terms"], i["rgi_criteria"]])

def get_prevalence_data_dask(f, accession):
    """
    Parse tabular index file to pull accession and prevalence
    """
    dask_df = dd.read_csv(f,sep='\t',dtype='object').compute()
    data = dask_df.loc[ dask_df['ncbi_accession'] == accession]
    dict = data.to_dict()
    return list(dict["aro_term"].values()), list(dict["rgi_criteria"].values())

def get_prevalence_data(f):
    """
    Load the whole tabular file
    """
    j = {}
    try:
        with open(os.path.join(f), 'r') as jfile:
            j = json.load(jfile)
    except Exception as e:
        print(e)
        exit()
    return j

def create_parser():
    parser = argparse.ArgumentParser(prog="parse_prevalence_data.py", description="Parser")
    parser.add_argument('-i', '--accession_json', required=False, help='json file with accessions')
    parser.add_argument('-p', '--prevalence_index', required=False, help='tabular file (index-for-model-sequences.txt)')
    parser.add_argument('-o', '--output_file', required=False, help='output file')
    return parser

def run():
	parser = create_parser()
	args = parser.parse_args()
	main(args)

if __name__ == "__main__":
	run()
