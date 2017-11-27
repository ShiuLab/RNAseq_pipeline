print('''
inp1 - File with list of SRA file names
        Entries should be an NCBI "run" identifier
        These often start with "SRR"
        Entries can be comma-delimited or individual
''')
import os,sys,fn

sra_list_file = sys.argv[1]

def retrieve_sra_file(file_name):
        first_three = file_name[0:3]
        first_six = file_name[0:6]
        os.system("wget ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/\
reads/ByRun/sra/%s/%s/%s/%s" % (first_three,first_six,file_name,file_name+".sra"))

sra_list = fn.file2list(sra_list_file)
print (sra_list)
for row in sra_list:
        if not row.startswith("#"):
                file_nms = row.split(",")
                for sra_file_nm in file_nms:
                        retrieve_sra_file(sra_file_nm.replace(".sra",""))
