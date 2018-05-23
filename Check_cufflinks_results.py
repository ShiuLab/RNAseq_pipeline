import os,sys
import os.path
# MAIN
print('''

inp1 = folder including cufflinks files
inp2 = folder to save output cufflink and htseq results with SRR name
inp3 = 0 for regular, 1 for pseudogene

''')
inp1 = sys.argv[1] #folder including cufflinks directories
inp2 = sys.argv[2] #output folder
inp3 = int(sys.argv[3])
os.chdir("%s" %inp1)
oup = open("missing_cufflinks_results", "w")
#oup.write("#!/bin/sh -login\n#PBS -q main\n")
#oup.write("#PBS -l nodes=1:ppn=1,walltime=3:59:00,mem=10gb\n")
#oup.write("#PBS -d %s\n" % inp4)
#oup.write("module load cufflinks\n\n")

if inp3 == 0:
    for file in os.listdir(inp1):
        if file.endswith(".sra_tophat"):
            dir2 = "%s/%s" %(inp1, file)
            name = file.split("_")[0].replace(".sra", "")
            if os.path.exists("%s/uniquecufflinks/genes.fpkm_tracking" %file):
                os.system("cp %s/uniquecufflinks/genes.fpkm_tracking %s/uniquecufflinks/%s_genes.fpkm_tracking" % (dir2, dir2, name))
                #oup.write("module load cufflinks; cufflinks -p 1 -I 5000 -o %s_cufflinks -G %s -b %s %s/accepted_hits.unique.sam\n" %(file, inp2, inp3, file))
            if os.path.exists("%s/HTSeqCount_%s.out" % (dir2, name)):
                os.system("cp %s/HTSeqCount_%s.out %s/%s_htseq_counts" % (dir2, name, dir2, name))
            else:
                oup.write("%s\n" %name)
            os.system("mv %s/uniquecufflinks/*_genes.fpkm_tracking %s" %(dir2,inp2))
            os.system("mv %s/*_htseq_counts %s" %(dir2,inp2))
            
    oup.close()
    

if inp3 == 1:
    for file in os.listdir(inp1):
        if file.endswith(".sra_tophat"):
            name = file.split("_")[0].replace(".sra", "")
            #print (name)
            dir2 = "%s/%s/pseudogene/" % (inp1, file)
            #print (dir2)
            if os.path.exists("%suniquecufflinks_ps/genes.fpkm_tracking" % dir2):
                os.system("cp %suniquecufflinks_ps/genes.fpkm_tracking %suniquecufflinks_ps/%s_ps_genes.fpkm_tracking" % (dir2, dir2, name))
                #oup.write("module load cufflinks; cufflinks -p 1 -I 5000 -o %s_cufflinks -G %s -b %s %s/accepted_hits.unique.sam\n" %(file, inp2, inp3, file))
                os.system("mv %suniquecufflinks_ps/*_ps_genes.fpkm_tracking %s" %(dir2, inp2))
                
            if os.path.exists("%sHTSeqCount_ps_%s.out" % (dir2, name)):
                os.system("cp %sHTSeqCount_ps_%s.out %s%s_ps_htseq_counts" % (dir2, name, dir2,name))
                os.system("mv %s*_ps_htseq_counts %s" %(dir2, inp2))
            else:
                oup.write("%s\n" %name)
            
    oup.close()
    
    
    
else:
    print ("need 0 for regular or 1 for pseudogenes")
    sys.exit()
