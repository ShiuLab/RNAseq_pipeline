import os,sys
import os.path
# MAIN
print('''

inp1 = folder including cufflinks files
inp2 = folder to save output cufflink and htseq results with SRR name

''')
inp1 = sys.argv[1] #folder including cufflinks directories

os.chdir("%s" %inp1)
oup = open("missing_cufflinks_results", "w")
#oup.write("#!/bin/sh -login\n#PBS -q main\n")
#oup.write("#PBS -l nodes=1:ppn=1,walltime=3:59:00,mem=10gb\n")
#oup.write("#PBS -d %s\n" % inp4)
#oup.write("module load cufflinks\n\n")

for file in os.listdir(inp1):
    if file.endswith(".sra_tophat"):
        name = file.split("_")[0].replace(".sra", "")
        if os.path.exists("%s/uniquecufflinks/genes.fpkm_tracking" %file):
            os.system("cp %s/uniquecufflinks/genes.fpkm_tracking %s_genes.fpkm_tracking" % (file, name))
            #oup.write("module load cufflinks; cufflinks -p 1 -I 5000 -o %s_cufflinks -G %s -b %s %s/accepted_hits.unique.sam\n" %(file, inp2, inp3, file))
        if os.path.exists("%s/HTSeqCount_%s.out" % (file, name)):
            os.system("cp %s/HTSeqCount_%s.out %s_htseq_counts" % (file, name, name))
        else:
            oup.write("%s\n" %name)
oup.close()

os.system("mv *_genes.fpkm_tracking %s" %inp2)
os.system("mv *_htseq_counts %s" %inp2)
