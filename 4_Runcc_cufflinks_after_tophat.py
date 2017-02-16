import os,sys
# MAIN
def print_help():
	print('''
Inputs:
    
inp1 = folder including tophat directories
inp2 = gff file (/mnt/scratch/peipeiw/tomato_transcriptome/Solanum_lycopersicum_GCF_000188115.3_S.lycopersicum.2.50_genomic.gff)
inp3 = genome.fa file (/mnt/scratch/peipeiw/tomato_transcriptome/Solanum_lycopersicum_GCF_000188115.3_SL2.50_genomic.fna)
inp4 = SE (0) or PE (1)

Required Modules:
    Samtools
''')

oup = open("runcc_cufflinks_htseq", "w")

def get_sam_write_script(inp1, inp2, inp3, inp4, oup):
    if inp4 == 1:
        for file in os.listdir(inp1):
            if file.endswith(".sra_tophat"):
                file1= file.strip().split(".")[0]
                filepath= inp1+"/"+file+"/"
            
                print ("converting unique sam to unique bam")
                os.system("samtools view -bS %saccepted_hits.unique.sam > %saccepted_hits.unique.bam"%(filepath, filepath))
                print ("sorting unique bam and convert back to sam")
                os.system("samtools sort -O sam -T accepted_hits.unique.sorted -o %saccepted_hits.unique.sorted.sam -n %saccepted_hits.unique.bam"%(filepath, filepath))
                print ("writing cufflinks script on unique.sam")
                oup.write("module load cufflinks; cufflinks -p 1 -I 5000 -o %suniquecufflinks -G %s -b %s %saccepted_hits.unique.sam\n" %(filepath, inp2, inp3, filepath))
                print ("writing HTseq script on sorted.unique.sam")
                oup.write("module load HTSeq; python -m HTSeq.scripts.count -m union -s no -t gene -i ID %saccepted_hits.unique.sorted.sam %s > %sHTSeqCount_%s.out\n" %(filepath, inp2, filepath, file1))
    else:
        for file in os.listdir(inp1):
            if file.endswith(".sra_tophat"):
                oup.write("module load cufflinks; cufflinks -p 1 -I 5000 -o %suniquecufflinks -G %s -b %s %saccepted_hits.unique.sam\n" %(filepath, inp2, inp3, filepath))
                oup.write("module load HTSeq; python -m HTSeq.scripts.count -m union -s no -t gene -i ID %saccepted_hits.unique.sam %s > %sHTSeqCount_%s.out\n" %(filepath, inp2, file1))

def main():
	if len(sys.argv) < 5 or "-h" in sys.argv:
	    print_help()
	    sys.exit()
	
	try:
	    inp1 = sys.argv[1] #folder including tophat files
            inp2 = sys.argv[2] #gff file
            inp3 = sys.argv[3] #genome.fa file
            inp4 = int(sys.argv[4]) #SE (0), PE (1)


	except:
	    print_help()
	    print ("Error reading arguments, quitting!")
	    sys.exit()
	
	oup = open("%s/runcc_cufflinks_htseq" %(inp1, "w"))
	get_sam_write_script(inp1, inp2, inp3, inp4, oup)
	oup.close()

if __name__ == "__main__":
	main()        
        

   
