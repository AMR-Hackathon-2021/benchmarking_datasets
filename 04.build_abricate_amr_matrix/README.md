```bash
#Download reads
fastq-dump --split-siles {SRA accession}

#Assemble
shovill --R1 {SRA accession}_1.fastq --R2 {SRA accession}_2.fastq --outdir assemblies/spades/{SRA accession} --cpus 15 --assembler spades
shovill --R1 {SRA accession}_1.fastq --R2 {SRA accession}_2.fastq --outdir assemblies/skesa/{SRA accession} --cpus 15 --assembler skesa

#Calc Assembly stats
quast -o assemblies/spades/{SRA accession}/quast assemblies/spades/{SRA accession}/contigs.fa

#MAP Reads and call SNPs
snippy --R1  {SRA accession}_1.fastq --R2  {SRA accession}_2.fastq  --outdir snippy/{biosample} --cpus 8 --reference {assembly acs}_genomic.fna

#Get Variants 
snippy-core --ref {assembly acs}_genomic.fna snippy/{biosample}    
##   - grab the sample info from stderr

#Get No coverage regions from bam file
bedtools genomecov -ibam snippy/{biosample}/snps.bam|grep -E "\s+0\s+"

#Get Mapped Reads
samtools sort --threads 8 -T {biosample} -n -o {biosample}/snps.sorted.bam SAMN02568587/snps.bam && bedtools bamtofastq -i {biosample}/snps.sorted.bam -fq {biosample}_1.fastq -fq2 {biosample}_2.fastq
##   - Need to sort by read name for bam2fastq to work correctly

#Abricate detection of AMR genes
abricate --db ncbi assemblies/spades/{SRA accession}/contigs.fa > assemblies/spades/{SRA accession}/abricate.{SRA accession}.ncbi.txt
abricate --db ncbi assemblies/skesa/{SRA accession}/contigs.fa > assemblies/skesa/{SRA accession}/abricate.{SRA accession}.ncbi.txt
abricate --db ncbi {assembly acs}_genomic.fna > abricate.{biosample}.ncbi.txt

#Build AMR gene presence absence matrix
abricate --summary {*abricate result files} > matrix.txt
```

#### Observations

* `SRA accession` comes from the `2021-11-12-Genomes.txt` list
* `2021-11-12-Genomes.txt` list was created by hand since NCBI does not offer links easily

#### Comments by James when creating (and updating) file `2021-11-12-Genomes.txt`
```text
I have filtered some of the genomes from the original set since they were not actually complete. These genomes have been run through the MOB-suite to label the different accessions as chromosome.
...
I have updated the datasheet to remove two genomes which the raw reads clearly are not from the closed assembly as well as added in mlst info
```
Shared through https://github.com/AMR-Hackathon-2021/benchmarking_datasets/issues/3

