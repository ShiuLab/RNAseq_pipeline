import os,sys
# MAIN
print('''

inp1 = folder including tophat directories
inp2 = gff file
inp3 = genome.fa file
inp4 = directory to work

''')
inp1 = sys.argv[1] #folder including tophat files
inp2 = sys.argv[2] #gff file
inp3 = sys.argv[3] #genome.fa file
inp4 = sys.argv[4] # directory to work
os.chdir("%s" %inp4)
oup = open("runcc_cufflinks", "w")
#oup.write("#!/bin/sh -login\n#PBS -q main\n")
#oup.write("#PBS -l nodes=1:ppn=1,walltime=3:59:00,mem=10gb\n")
#oup.write("#PBS -d %s\n" % inp4)
#oup.write("module load cufflinks\n\n")

for file in os.listdir(inp1):
    if file.endswith(".sra_tophat"):
        oup.write("module load cufflinks; cufflinks -p 1 -I 5000 -o %s_cufflinks -G %s -b %s %s/accepted_hits.unique.sam\n" %(file, inp2, inp3, file))

oup.close()   
