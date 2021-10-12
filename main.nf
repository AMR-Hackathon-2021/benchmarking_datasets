#!/usr/bin/env nextflow
params.eskape = "$baseDir/data/ESKAPE_FDA-ARGOS_complete_genomes.txt"
params.outdir = "$baseDir/nf_output"

eskape_file = file(params.eskape)
// nextflow.preview.dsl = 2

/***  from get_accessions/  ***/
process get_accession_file {
  publishDir "${params.outdir}", mode: 'copy', overwrite: true
  input:
    path eskape from params.eskape
  output:
		file("assembly_accession.txt") into summary_ch
		file("assembly_accession.txt") into download_ch 
  shell:
    '''
    cat !{params.eskape} | cut -f1 | grep -v "# Assembly" > assembly_accession.txt 
    '''
}

/***  from get_accessions/  ***/
process summary {
  conda "ncbi-datasets-cli"
  publishDir "${params.output}", mode: 'copy', overwrite: true
  input:
    file (access) from summary_ch
  output:
		file("all.json")
  shell:
    '''
    datasets summary genome accession --inputfile !{access} > all.json
    '''
}

/***  from get_accessions/  ***/
process download {
  conda "ncbi-datasets-cli"
  publishDir "${params.output}", mode: 'copy', overwrite: true
  input:
    file (access) from download_ch 
  output:
		file("ncbi_dataset.zip")
  shell:
    '''
    datasets download genome accession --inputfile assembly_accession.txt --exclude-gff3 --exclude-protein --exclude-rna
    '''
}

/***  from get_reference_data/    ***/
process download_CARD_canonical_data {
  publishDir "${params.output}", mode: 'copy', overwrite: true
  shell:
  '''
  wget -O data --no-check-certificate https://card.mcmaster.ca/latest/data
  mkdir -p card_data
  tar xf data -C card_data
  rm data
  '''
}

/***  from get_reference_data/    ***/
process download_CARD_variants_data {
  publishDir "${params.output}", mode: 'copy', overwrite: true
  shell:
  '''
  echo "=================================== DOWNLOAD CARD VARIANTS DATA ==================================="
  wget -O variants --no-check-certificate https://card.mcmaster.ca/latest/variants
  mkdir -p card_variants
  tar xf variants -C card_variants
  gunzip card_variants/*.gz
  rm variants
  '''
}
