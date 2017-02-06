## IMPORT
import sys
import os

## MAIN
print ('''
inp1 = .sra file
inp2 = bowtie index root name
inp3 = paired (1) or single reads (0)

Optional Inputs:
	-trim_threads = threads to use when running Trimmomatic (note: the actual number of threads used will be 1 + this value)
	-trim_adapter = adapter sequenecs to use with Trimmomatic
	-trim_seed = seed size to use with adapter trimming
	-trim_pclip = palidromic clipping to use with adapter trimming
	-trim_sclip = simple clipping to used with adapter trimming
	-trim_leading = quality value for hard clipping of leading bases
	-trim_trailing = quality value for hard clipping of trailing bases
	-trim_winsize = window size for soft clipping
	-trim_winqual = average quality for soft clipping
	-trim_minlen = minimum length of trimmed reads
	-trim_crop = fixed number of bases to trim from the front of all reads
	-trim_hcrop = fixed number of bases to trim form the end of all reads
	-tophat_threads = number of threads to use with tophat 
	-min_intron = minimum intron size to use with tophat and cufflinks, default = 50
	-max_intron = maximum intron size to use with tophat and cufflinks, default = 5000
	-max_multihit = maximum number of mappings per read in tophat, default = 20
	-filter_min_len = minimum read length post-trimming, default = 20
	-filter_min_phred = minimum average read phred post-trimming, default = 20

Protocol:
	fastq-dump: covert SRA -> fastq
	Trimmomatic: trim fastq
	Filter reads by length and min ave phred score
	Bowtie: map reads
	SAMTools: Convert bam file to sam file
	Filter sam file to primary and unique reads
  
Required Modules:
	- SRAToolkit (module load SRAToolkit)
	- Trimmomatic (module load Trimmomatic)
	- Tophat2 (module load TopHat2)
	- Boost (module load Boost)
	- SAMTools (module load SAMTools)
	
	module load SRAToolkit; module load Trimmomatic; module load TopHat2; module load Boost; module load SAMTools
''')

## READ INPUT SRA
infile = os.path.abspath(sys.argv[1])
genome = sys.argv[2]
PE = int(sys.argv[3])

## PRESET VALUES

# out_dir = ""

# Trimmomatic Parameters-- Always used 
# updating adapter_seq to include all universal adaptors, need to have these in wd
if PE == 1:
	adapter_seq = "all_PE_adapters.fa"
else:
	adapter_seq = "all_SE_adapters.fa"
trim_threads = 4
seed_mismatches = 2 
palindrome_clip = 30
simple_clip = 10
leading = 3
trailing = 3 
window_size = 4
window_quality = 20

# Trimmomatic Parameters-- Added when value is non-zero
trim_minlen = 0
trim_crop = 0
trim_headcrop = 0

# Default filtering thresholds
min_filter_len = 20
min_filter_phred = 20

# Tophat&Cufflinks Parameters
tophat_threads = 8
min_intron_size = 50
max_intron_size = 5000
max_multiHits = 20 

## READ PARAMETERS
for i in range(len(sys.argv)):
	# if sys.argv[i] == "-genome":
		# genome = sys.argv[i+1]
	if sys.argv[i] == "-gff":
		gff = sys.argv[i+1]
	if sys.argv[i] == "-trim_threads":
		trim_threads = sys.argv[i+1]
	if sys.argv[i] == "-trim_adapter":
		adapter_seq = sys.argv[i+1]
	if sys.argv[i] == "-trim_seed":
		seed_mismatches = sys.argv[i+1]
	if sys.argv[i] == "-trim_pclip":
		palindrome_clip = sys.argv[i+1]
	if sys.argv[i] == "-trim_sclip":
		simple_clip = sys.argv[i+1]
	if sys.argv[i] == "-trim_leading":
		leading = sys.argv[i+1]
	if sys.argv[i] == "-trim_trailing":
		trailing = sys.argv[i+1]
	if sys.argv[i] == "-trim_winsize":
		window_size = sys.argv[i+1]
	if sys.argv[i] == "-trim_winqual":
		window_quality = sys.argv[i+1]
	if sys.argv[i] == "-trim_minlen":
		trim_minlen = sys.argv[i+1]
	if sys.argv[i] == "-trim_crop":
		trim_crop = sys.argv[i+1]
	if sys.argv[i] == "-trim_hcrop":
		trim_headcrop = sys.argv[i+1]
	if sys.argv[i] == "-tophat_threads":
		tophat_threads = sys.argv[i+1]
	if sys.argv[i] == "-min_intron":
		min_intron_size = sys.argv[i+1]
	if sys.argv[i] == "-max_intron":
		max_intron_size = sys.argv[i+1]
	if sys.argv[i] == "-max_multihit":         
		max_multiHits = sys.argv[i+1]
	if sys.argv[i] == "-filter_min_len":    
		min_filter_len = sys.argv[i+1]
	if sys.argv[i] == "-filter_min_phred":   
		min_filter_phred = sys.argv[i+1]
	# if sys.argv[i] == "-output_dir":   
		# out_dir = os.path.abspath(sys.argv[i+1])


## RUN COMMANDS
# Decompress SRA Files
f_sra = infile
print ("Dumping SRA file")
if PE == 1:
	dump_command = "fastq-dump --split-files "+f_sra
else:
	dump_command = "fastq-dump "+f_sra
# print dump_command
os.system(dump_command)

print ("First fastQC")
if PE == 1:
	f_fastq = infile.split(".")[0]+"_1.fastq"
	r_fastq = infile.split(".")[0]+"_2.fastq"
	print (infile, f_fastq, r_fastq)
	fastqc_command1 = "fastqc -f fastq "+ f_fastq
	fastqc_command2 = "fastqc -f fastq "+ r_fastq
	os.system(fastqc_command1)
	os.system(fastqc_command2)
else:
	f_fastq = infile.split(".")[0]+".fastq"
	print (infile, f_fastq)
	fastqc_command = "fastqc -f fastq "+ f_fastq
	os.system(fastqc_command)

print ("Trimming reads")
# Trim Reads
if PE==1:
	f_fastq = infile.split(".")[0]+"_1.fastq"
	r_fastq = infile.split(".")[0]+"_2.fastq"
	print (infile, f_fastq, r_fastq)
	f_fastq_trimmedP =  infile.split(".")[0]+"_1trimmed.fastq"
	r_fastq_trimmedP =  infile.split(".")[0]+"_2trimmed.fastq"
	f_fastq_trimmedU =  infile.split(".")[0]+"_1Utrimmed.fastq"
	r_fastq_trimmedU =  infile.split(".")[0]+"_2Utrimmed.fastq"
	trimmomatic_command = "java -jar $TRIM/trimmomatic PE -threads %s %s %s %s %s %s %s " % (trim_threads,f_fastq,r_fastq, f_fastq_trimmedP, f_fastq_trimmedU, r_fastq_trimmedP, r_fastq_trimmedU)
	trimmomatic_command = trimmomatic_command + "ILLUMINACLIP:/mnt/home/uygunsah/1_Expression_Database/RNAseq/%s:%s:%s:%s " % (adapter_seq,seed_mismatches,palindrome_clip,simple_clip)
	trimmomatic_command = trimmomatic_command + "LEADING:%s TRAILING:%s SLIDINGWINDOW:%s:%s" % (leading,trailing,window_size,window_quality)
	if not trim_minlen == 0:
		trimmomatic_command = trimmomatic_command + " MINLEN:%s" (trim_minlen)
	if not trim_crop == 0:
		trimmomatic_command = trimmomatic_command + " CROP:%s" (trim_crop)
	if not trim_headcrop == 0:
		trimmomatic_command = trimmomatic_command + " HEADCROP:%s" (trim_headcrop)
	os.system(trimmomatic_command)
	print ("    Deleting original fastq file:")
	print ("    %s"%(f_fastq))
	os.system("rm %s"%(f_fastq))
	os.system("rm %s"%(r_fastq))
	print ("Filtering trimmed reads")
	# Filter trimmed reads
	filter_command1 = "python /mnt/home/lloydjo1/scripts/A_Small_Read_Processing/filter_fastq.py -i %s -min %s -ave %s"%(f_fastq_trimmedP,min_filter_len,min_filter_phred)
	filter_command2 = "python /mnt/home/lloydjo1/scripts/A_Small_Read_Processing/filter_fastq.py -i %s -min %s -ave %s"%(r_fastq_trimmedP,min_filter_len,min_filter_phred)

	# print filter_command
	os.system(filter_command1)
	os.system(filter_command2)
	# filtered_file = f_fastq_trimmed.replace("fastq","")+str(min_filter_len)+"_min_len."+str(min_filter_len)+"_min_phred.fastq"
	filtered_file1 = f_fastq_trimmedP.replace(".fastq","")+"_1.filtered.fastq"
	filtered_file2 = r_fastq_trimmedP.replace(".fastq","")+"_2.filtered.fastq"
	print ("    Deleting trimmed fastq file:")
	print ("    %s"%(f_fastq_trimmed))
	os.system("rm %s"%(f_fastq_trimmedP))
	os.system("rm %s"%(f_fastq_trimmedP))

	print ("Second fastQC")
	f_fastq2 = filtered_file1
	r_fastq2 = filtered_file2
	fastqc_command1 = "fastqc -f fastq "+ f_fastq2
	fastqc_command2 = "fastqc -f fastq "+ r_fastq2
	os.system(fastqc_command1)
	os.system(fastqc_command2)
	print ("Running TopHat")
	# Run tophat
	f_tophat_file = infile.split(".")[0]+".sra_tophat" #naming file

	# if out_dir != "":
		# f_tophat_file = out_dir+"/"+f_tophat_file

	tophat_command = "tophat2 -p %s -i %s -I %s -g %s -o %s %s %s" % (tophat_threads,min_intron_size,max_intron_size,max_multiHits,f_tophat_file,genome,filtered_file1, filtered_file2) #command
	print (tophat_command)
	os.system(tophat_command)
	#print ("    Deleting filtered fastq file:")
	print ("    %s"%(filtered_file))
	#os.system("rm %s"%(filtered_file))

	print ("Converting BAM to SAM")
	os.system("python /mnt/home/lloydjo1/scripts/A_Small_Read_Processing/bam2sam.py %s/accepted_hits.bam"%(f_tophat_file))

	print ("Filtering SAM to primary and unique reads")
	os.system("python /mnt/home/lloydjo1/scripts/A_Small_Read_Processing/primary_and_unique_mapped_reads.py %s/accepted_hits.sam"%(f_tophat_file))

else:
	f_fastq = infile.split(".")[0]+".fastq"
	print (infile, f_fastq)
	f_fastq_trimmed =  infile.split(".")[0]+"trimmed.fastq"

	trimmomatic_command = "java -jar $TRIM/trimmomatic SE -threads %s %s %s " % (trim_threads,f_fastq,f_fastq_trimmed)
	trimmomatic_command = trimmomatic_command + "ILLUMINACLIP:/mnt/home/uygunsah/1_Expression_Database/RNAseq/%s:%s:%s:%s " % (adapter_seq,seed_mismatches,palindrome_clip,simple_clip)
	trimmomatic_command = trimmomatic_command + "LEADING:%s TRAILING:%s SLIDINGWINDOW:%s:%s" % (leading,trailing,window_size,window_quality)
	if not trim_minlen == 0:
		trimmomatic_command = trimmomatic_command + " MINLEN:%s" (trim_minlen)
	if not trim_crop == 0:
		trimmomatic_command = trimmomatic_command + " CROP:%s" (trim_crop)
	if not trim_headcrop == 0:
		trimmomatic_command = trimmomatic_command + " HEADCROP:%s" (trim_headcrop)

	# print trimmomatic_command
	os.system(trimmomatic_command)
	print ("    Deleting original fastq file:")
	print ("    %s"%(f_fastq))
	os.system("rm %s"%(f_fastq))

	print ("Filtering trimmed reads")
	# Filter trimmed reads
	filter_command = "python /mnt/home/lloydjo1/scripts/A_Small_Read_Processing/filter_fastq.py -i %s -min %s -ave %s"%(f_fastq_trimmed,min_filter_len,min_filter_phred)
	# print filter_command
	os.system(filter_command)
	# filtered_file = f_fastq_trimmed.replace("fastq","")+str(min_filter_len)+"_min_len."+str(min_filter_len)+"_min_phred.fastq"
	filtered_file = f_fastq_trimmed.replace(".fastq","")+".filtered.fastq"
	print ("    Deleting trimmed fastq file:")
	print ("    %s"%(f_fastq_trimmed))
	os.system("rm %s"%(f_fastq_trimmed))

	print ("Second fastQC")
	f_fastq2 = filtered_file
	fastqc_command = "fastqc -f fastq "+ f_fastq2
	os.system(fastqc_command)

	print ("Running TopHat")
	# Run tophat
	f_tophat_file = infile.split(".")[0]+".sra_tophat" #naming file

	# if out_dir != "":
		# f_tophat_file = out_dir+"/"+f_tophat_file

	tophat_command = "tophat2 -p %s -i %s -I %s -g %s -o %s %s %s" % (tophat_threads,min_intron_size,max_intron_size,max_multiHits,f_tophat_file,genome,filtered_file) #command
	print (tophat_command)
	os.system(tophat_command)
	#print ("    Deleting filtered fastq file:")
	print ("    %s"%(filtered_file))
	#os.system("rm %s"%(filtered_file))

	print ("Converting BAM to SAM")
	os.system("python /mnt/home/lloydjo1/scripts/A_Small_Read_Processing/bam2sam.py %s/accepted_hits.bam"%(f_tophat_file))

	print ("Filtering SAM to primary and unique reads")
	os.system("python /mnt/home/lloydjo1/scripts/A_Small_Read_Processing/primary_and_unique_mapped_reads.py %s/accepted_hits.sam"%(f_tophat_file))
