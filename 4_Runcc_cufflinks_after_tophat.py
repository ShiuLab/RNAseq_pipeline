import os,sys
# MAIN
print('''

inp1 = folder including tophat directories
inp2 = gff file (/mnt/scratch/peipeiw/tomato_transcriptome/Solanum_lycopersicum_GCF_000188115.3_S.lycopersicum.2.50_genomic.gff)
inp3 = genome.fa file (/mnt/scratch/peipeiw/tomato_transcriptome/Solanum_lycopersicum_GCF_000188115.3_SL2.50_genomic.fna)
inp4 = directory to output
inp5 = all mapped reads(0) or unique mapped reads (1)

''')
inp1 = sys.argv[1] #folder including tophat files
inp2 = sys.argv[2] #gff file
inp3 = sys.argv[3] #genome.fa file
inp4 = sys.argv[4] # directory to work
inp5 = int(sys.argv[5])

os.chdir("%s" %inp4)
oup = open("runcc_cufflinks_htseq", "w")

if inp5 == 1:
    for file in os.listdir(inp1):
        if file.endswith(".sra_tophat"):
            oup.write("module load cufflinks; cufflinks -p 1 -I 5000 -o %s_uniquecufflinks -G %s -b %s %s/accepted_hits.unique.sam\n" %(file, inp2, inp3, file))
            oup.write("module load HTSeq; python -m HTSeq.scripts.count -m union -s no -t gene -i ID %s/accepted_hits.unique.sam %s > %s_htseq_uniquecounts\n" %(file, inp2, file.split(".")[0]))
else:
    for file in os.listdir(inp1):
        if file.endswith(".sra_tophat"):
            oup.write("module load cufflinks; cufflinks -p 1 -I 5000 -o %s_allcufflinks -G %s -b %s %s/accepted_hits.sam\n" %(file, inp2, inp3, file))
            oup.write("module load HTSeq; python -m HTSeq.scripts.count -m union -s no -t gene -i ID %s/accepted_hits.sam %s > %s_htseq_allcounts\n" %(file, inp2, file.split(".")[0]))

oup.close()   
