#!/usr/bin/env nextflow
params.table = "$baseDir/list_of_genomes.tsv"
params.outdir = './output'
table = file (params.table)

Channel
    .fromPath(table)
    .splitCsv(header:true, sep:'\t')
    .map{ row-> tuple(row.sra_run_acs, row.refseq_ftp) }  /* I only need sra_run_acs? there are dups since chrom + plasmid */
    .set { sra_table_ch }

process download_reads {
  publishDir "${params.outdir}", mode: 'copy', overwrite: true
  tag {SRA}
  input:
    set val(SRA), val(link) from sra_table_ch
  output:
		val(SRA) into shovill_spades_ch 
  shell:
    '''
    echo !{SRA} > boi 
    '''
}

process shovill_spades {
  publishDir "${params.outdir}", mode: 'copy', overwrite: true
  input:
		val(SRA) from shovill_spades_ch 
  output:
		file("${SRA}")
  shell:
    '''
    touch !{SRA}
    '''
}
