#!/usr/bin/env nextflow
params.table = "$baseDir/list_of_genomes.tsv"
params.outdir = "$baseDir/output"
table = file (params.table)


Channel
    .fromPath(table)
    .splitCsv(header:true, sep:'\t')
    .map{ row-> tuple(row.sra_run_acs, row.refseq_ftp) }  /* I only need sra_run_acs? */
    .set { sra_table_ch }


process download_reads {
  conda "parallel-fastq-dump"
  publishDir "${params.outdir}", mode: 'copy', overwrite: true
  input:
    set SRA, link from sra_table_ch
  output:
		set ${SRA}, file("${SRA}_1.fastq"), file("${SRA}_2.fastq"),  into shovill_spades_ch 
		set ${SRA}, file("${SRA}_1.fastq"), file("${SRA}_2.fastq"),  into shovill_skesa_ch 
  shell:
    '''
    fastq-dump --split-siles !{SRA}
    '''
}

process shovill_spades {
  conda "shovill"
  publishDir "${params.output}", mode: 'copy', overwrite: true
  input:
		set SRA, file(f1), file(f2),  from shovill_spades_ch 
  output:
		file("spades/${SRA}") into out_spades_ch
  shell:
    '''
    shovill --R1 !{f1} --R2 !{f2} --outdir spades/!{SRA} --cpus !{task.cpus} --assembler spades
    '''
}

process shovill_skesa {
  conda "shovill"
  publishDir "${params.output}", mode: 'copy', overwrite: true
  input:
		set SRA, file(f1), file(f2),  from shovill_skesa_ch 
  output:
		file("skesa/${SRA}") into out_skesa_ch
  shell:
    '''
    shovill --R1 !{f1} --R2 !{f2} --outdir spades/!{SRA} --cpus !{task.cpus} --assembler skesa
    '''
}
