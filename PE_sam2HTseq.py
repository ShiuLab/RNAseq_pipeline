import os,sys

def print_help():
	print('''
Inputs:
inp1 = folder including tophat directories
inp2 = 0 for SE, 1 for PE
inp3 = gff file
inp4 = genome.fa file

Required Modules:
    Samtools
''')


def get_sam_write_script(inp1, inp2, inp3, inp4, oup):
    for dir1 in os.listdir(inp1):
        if dir1.endswith(".sra_tophat"):
            file1= dir1.strip().split(".")[0]
            filepath= inp1+"/"+dir1+"/"
            print (file1)
            print (filepath)

            print ("getting unique reads from SAM file")
            os.system("python /mnt/home/john3784/Github/RNAseq_pipeline/primary_and_unique_mapped_reads2.py %saccepted_hits.sam %s"%(filepath, inp2))
        
            print ("converting unique sam to unique bam")
            os.system("samtools view -bS %saccepted_hits.unique.sam > %saccepted_hits.unique.bam"%(filepath, filepath))
        
            print ("sorting unique bam and convert back to sam")
            os.system("samtools sort -O sam -T accepted_hits.unique.sorted -o %saccepted_hits.unique.sorted.sam -n %saccepted_hits.unique.bam"%(filepath, filepath))
        
            print ("writing cufflinks script on sorted.unique.sam")
            oup.write("module load cufflinks; cufflinks -p 1 -I 5000 -o %s_uniquecufflinks -G %s -b %s %s/accepted_hits.unique.sorted.sam\n" %(filepath, inp3, inp4, filepath))
           
            print ("writing HTseq on sorted.unique.sam")
            oup.write("module load HTSeq; python -m HTSeq.scripts.count -m union -s no -t gene -i ID -r name %saccepted_hits.unique.sorted.sam %s > %sHTSeqCount_%s.out\n"%(filepath, inp3, filepath, file1))
        
def main():
	if len(sys.argv) < 4 or "-h" in sys.argv:
	    print_help()
	    sys.exit()
	
	try:
	    inp1 = sys.argv[1] #folder including tophat files
	    inp2 = sys.argv[2] # 0 for SE, 1 for PE
	    inp3 = sys.argv[3] #gff file
	    inp4 = sys.argv[4] #genome.fa file


	except:
	    print_help()
	    print ("Error reading arguments, quitting!")
	    sys.exit()
	
	oup = open("%s/runcc_cufflinks_htseq" %(inp1, "w"))
	get_sam_write_script(inp1, inp2, inp3, inp4, oup)

if __name__ == "__main__":
	main()        
        