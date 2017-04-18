# IMPORT
import os,sys

# MAIN
print('''

inp1 = file with list of SRA files
inp2 = bowtie index base (full path)
inp3 = SE (0) or PE (1) or paired processed as single (2)
inp3 and on:
	Any additional parameters for ProcessSRA_hpcc2.py
	These will be appended exactly as they appear 
''')

files = sys.argv[1]
bowtie_index = sys.argv[2]
SE = sys.argv[3]
out_cmd = "module load SRAToolkit; module load FastQC; module load Trimmomatic; \
module load TopHat2; module load Boost; module load SAMtools; module load python; \
python /mnt/home/john3784/Github/RNAseq_pipeline/\
ProcessSRA_hpcc2.py %s %s %s"
if len(sys.argv) > 4:
	additional_commands = " ".join(sys.argv[4:])
	out_cmd = out_cmd+" "+additional_commands

file_list = [f.strip() for f in open(files,"r").readlines()]
output = open(files+".runcc","w")
for file in file_list:
	output.write(out_cmd %(file, bowtie_index, SE)+"\n")
# out_commands = ["module load SRAToolkit; module load Trimmomatic; \
# module load TopHat2; module load Boost; python /mnt/home/lloydjo1/\
# Projects/7_intergenic_transcription_poaceae/_scripts/ProcessSRA_hpcc.py\ " + \
# f + " -genome " + bowtie_index + "\n" for f in file_list]
output.close()
