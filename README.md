# RNAseq pipeline

Workflow: Bowtie -> Tophat (maps reads) -> get sam file via samtools -> 
HTseq count [to get counts of reads to each gene or exon] -> Edge R -> differential expression  

# Needed files

1) Genome sequence in FASTA format

2) SRA file containing sequence reads (or folder with all SRA files and a file with a list of all SRAs you want to run)

3) GFF file for genome sequence

# Create Bowtie Index for Genome sequence: estimated time: ~15 minutes

1) load Tophat2 module

    module load Tophat2
    
2) Use bowtie2-build to build the index

    bowtie2-build [genome sequence fasta file] [base name for output files]
    
    bowtie2-build  Slycopersicum_390_v2.5.fa  Slycopersicum_390_v2.5
