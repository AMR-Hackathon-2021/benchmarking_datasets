#!/usr/bin/python3

"""
Purpose of this script is to inject a gene into the genome

"""
from Bio import SeqIO
from argparse import ArgumentParser
from random import randint

def count_contigs(genome):
    number_of_contigs = 0
    for contig in SeqIO.parse(genome, "fasta"):
        number_of_contigs += 1
    return number_of_contigs

def injectgene(gene, contig, border):
    lengthcontig = len(contig)

    if lengthcontig < 2*border:
        sys.exit('twice the bordersize is larger than the target contig to inject, aborting now')
    locationinjection = randint(0 + border, lengthcontig - border)
    newcontig = contig[:locationinjection] + gene + contig[locationinjection:]
    return newcontig

def write_genome(genomedict, outfile):
    for name, contig in zip(genomedict.keys(), genomedict.values()):
        print(f'>{name}\n{contig}')

    
def readgene(genefasta):
    for contig in SeqIO.parse(genefasta, 'fasta'):
        fasta = contig.seq
    return fasta


def injector(ingenome, gene, border, outgenome):
    numbercontigs = count_contigs(ingenome)
    target_contig = randint(0, numbercontigs)
    gene = readgene(gene)
    genome = {}
    for contignumber, contig in enumerate(SeqIO.parse(ingenome, 'fasta')):
        contigsequence = contig.seq

        if contignumber == target_contig:
            contigsequence = injectgene(gene, contig.seq, border) 
        genome[contig.id] = contigsequence

    write_genome(genome, outgenome)

    

def main(command_line = None):
    #add main parser object
    parser = ArgumentParser(description = "multifasta splitter")
    parser.add_argument("-i", required = True, dest = "input_file")
    parser.add_argument("-o", required = True, dest = "output_file")
    parser.add_argument("--gene", required = False, dest = "gene", type = str, help = "provide gene sequence here insert in the genome")
    parser.add_argument("--border", required = False, dest = "border", type = int, default = 500,  help = "How far should the inserted gene be from either edge of the contig?")


    args = parser.parse_args(command_line)

    injector(args.input_file, args.gene, args.border, args.output_file)

    #print(f'injected {args.gene} in {args.input_file} outputting to {args.output_file}')

if __name__ == "__main__":
    main()
