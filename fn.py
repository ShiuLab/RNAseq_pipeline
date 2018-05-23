### FILE MANAGEMENT
def get_files(dir,probe="",headtail=""):
	from os import path,listdir
	dir = path.abspath(dir)
	l = []
	for f in listdir(dir):
		if probe == "":
			l.append(dir+"/"+f)
		elif headtail == "":
			if probe in f:
				l.append(dir+"/"+f)
		elif headtail == "head":
			if f.startswith(probe):
				l.append(dir+"/"+f)
		elif headtail == "tail":
			if f.endswith(probe):
				l.append(dir+"/"+f)
		else:
			print "headtail argument not understood, headtail =",\
headtail
			print "\tvalid arguments: head, tail"
	return l

def convert_probe(probe_str):
	if "," in probe_str:
		probe,headtail = probe_str.split(",")
	else:
		probe = probe_str
		headtail = ""
	return probe,headtail

def transpose_file(file_name): #NumPy Required!
	import os
	os.system("python /mnt/home/lloydjo1/scripts/transpose.py %s"%file_name)
	os.system("mv %s.T %s"%(file_name,file_name))

def generate_line_indices(fl): # http://stackoverflow.com/questions/620367/python-how-to-jump-to-a-particular-line-in-a-huge-text-file
	line_offset = []
	offset = 0
	inp = open(fl)
	for line in inp:
		line_offset.append(offset)
		offset += len(line)
	inp.close()
	return line_offset
###
### FILE CONVERTERS
def file2list(inp_file,split_char="",keep_ind=""):
	inp = open(inp_file)
	l = []
	for line in inp:
		if split_char == "":
			l.append(line.strip())
		else:
			if keep_ind == "":
				l.append(line.strip().split(split_char))
			else:
				l.append(line.strip().split(split_char)\
[keep_ind])
	inp.close()
	return l

def file2set(inp_file,split_char="",keep_ind=""):
	inp = open(inp_file)
	s = set()
	for line in inp:
		if split_char == "":
			s.add(line.strip())
		else:
			if keep_ind == "":
				s.add(line.strip().split(split_char))
			else:
				s.add(line.strip().split(split_char)[keep_ind])
	inp.close()
	return s

def add_file2set(inp_file,add_set,split_char="",keep_ind=""):
	inp = open(inp_file)
	for line in inp:
		if split_char == "":
			s.add(line.strip())
		else:
			if keep_ind == "":
				s.add(line.strip().split(split_char))
			else:
				s.add(line.strip().split(split_char)[keep_ind])
	inp.close()

def file2dict(inp_file,split_char="\t",key_ind=0,val_ind=1):
	inp = open(inp_file)
	dict = {}
	for line in inp:
		if not line.startswith("#"):
			lineLst = line.strip().split(split_char)
			key = lineLst[key_ind]
			vals = lineLst[val_ind:]
			if key not in dict:
				dict[key] = vals
			else:
				dict[key] = dict[key]+vals
	inp.close()
	return dict
	
def file2dict_2col(inp_file,split_char="\t",key_ind=0,val_ind=1):
	inp = open(inp_file)
	dict = {}
	for line in inp:
		if not line.startswith("#"):
			lineLst = line.strip().split(split_char)
			# print lineLst
			key = lineLst[key_ind]
			val = lineLst[val_ind]
			if key not in dict:
				dict[key] = val
			else:
				print "WARNING: Multiple identical IDs encountered:",key,"| Most recent value kept" 
				dict[key] = val
	inp.close()
	return dict

def fasta2dict(fasta_file):
	dict = {}
	inp = open(fasta_file)
	for line in inp:
		if line.startswith(">"):
			header = line.strip().replace(">","")
			dict[header] = []
		else:
			dict[header].append(line.strip())
	return dict
###
### LIST FUNCTIONALITY
def transpose(array_style_list):
	import numpy
	
	max_len = 0
	for list in array_style_list:
		if len(list) > max_len:
			max_len = len(list)
	
	for list in array_style_list:
		while len(list) < max_len:
			list.append("")
	
	array = numpy.array(array_style_list)
	transposed = array.T
	
	return transposed

def list_of_lists(number):
	list = []
	while len(list) < int(number):
		list.append([])
	return list

def fill_empty_list_with_item(list,item,number):
	while len(list) < int(number):
		list.append(item)

def make_float_list(list,ignore_list=[],ignore_replace=""):
	import sys
	try:
		float_list = []
		for item in list:
			last_item = item
			if ignore_list == []:
				float_list.append(float(item))
			elif ignore_replace == "":
				if item not in ignore_list:
					float_list.append(float(item))
			else:
				if item in ignore_list:
					item = ignore_replace
				else:
					item = float(item)
				float_list.append(item)
		return float_list
	except:
		print "This item will not float:",last_item
		print "Aborted!"
		sys.exit()

def make_string_list(list):
	str_list = []
	for item in list:
		str_list.append(str(item))
	return str_list

def make_int_list(list):
	int_list = []
	for item in list:
		try:
			int_list.append(int(item))
		except:
			print "Item can not be integer:",item
			sys.exit()
	return int_list
###
### STRING FUNCTIONALITY
def clear_spaces(string): #returns tab-delimited
	string = string.strip()
	while "  " in string:
		string = string.replace("  "," ")
	string = string.replace(" ","\t")
	return string
###
### COORDINATES FUNCTIONALITY
def check_for_overlap(coords0_l,c0s_ind,c0e_ind,coords1_l,c1s_ind,c1e_ind): #returns True or False for overlap
	c0_start = int(coords0_l[c0s_ind])
	c0_end = int(coords0_l[c0e_ind])
	c1_start = int(coords1_l[c1s_ind])
	c1_end = int(coords1_l[c1e_ind])
	if c0_start <= c1_start and c0_end >= c1_start:
		ovrlp = True
	elif c1_start <= c0_start and c1_end >= c0_start:
		ovrlp = True
	else:
		ovrlp = False
	return ovrlp

def calc_percent_coverage(coords0_l,c0s_ind,c0e_ind,coords1_l,c1s_ind,c1e_ind): # calculates percent of region0 covered by region1
	# print "OVERLAP:"
	# print "\t".join(reg_ln_l)
	# print "\t".join(feat_ln_l)
	
	c0_start = int(coords0_l[c0s_ind])
	c0_end = int(coords0_l[c0e_ind])
	c0_tot_len = c0_end-c0_start+1
	c1_start = int(coords1_l[c1s_ind])
	c1_end = int(coords1_l[c1e_ind])	
	
	if c1_start <= c0_start and c1_end >= c0_end: #check if region0 is encompassed by region1
		coverage_start = c0_start
		coverage_end = c0_end
		# print "region0 is encompassed by region1"
	elif c0_start <= c1_start and c0_end >= c1_end: #check if region1 is encompassed by region0
		coverage_start = c1_start
		coverage_end = c1_end
		# print "region1 is encompassed by region0"
	elif c0_start < c1_start: #check if region0 starts first, keep back end of region0
		coverage_start = c1_start
		coverage_end = c0_end
		# print "back of region0 overlaps with front of region1"
	elif c1_start < c0_start: #check if region1 starts first, keep front end of region0
		coverage_start = c0_start
		coverage_end = c1_end
		# print "back of region1 overlaps with front of region0"
	else:
		print "Anything else??"
		print coords0_l
		print coords1_l
	
	coverage_length = coverage_end-coverage_start+1
	percent_of_total = round(float(coverage_length)/float(c0_tot_len)*100,2)
	
	# Check for abnormalities
	if percent_of_total > 100.0:
		print "COVERAGE OVER 100%"
		print reg_ln_l
		print feat_ln_l
		print percent_of_total
	elif percent_of_total <= 0:
		print "NEGATIVE COVERAGE"
		print "\t".join(reg_ln_l)
		print "\t".join(feat_ln_l)
		print percent_of_total
	# print "Cov length:",coverage_length
	# print "% coverage:",percent_of_total
	# print
	return percent_of_total
###
### BIOINFORMATICS COMMANDS

def run_fastq_dump(sra_id,layout): #requires SRAToolkit module | also returns name of generated FASTQ file
	import os
	if layout.lower() == "single":
		os.system("fastq-dump %s.sra"%(sra_id))
	elif layout.lower() == "paired":
		os.system("fastq-dump --split-3 %s.sra"%(sra_id))
		if os.path.isfile("%s_2.fastq"%sra_id) == True:
			os.system("rm %s_2.fastq"%sra_id)
		if os.path.isfile("%s.fastq"%sra_id) == True:
			os.system("rm %s.fastq"%sra_id)
		os.system("mv %s_1.fastq %s.fastq"%(sra_id,sra_id))
	return sra_id+".fastq"

def run_trimmomatic_calculon(fastq_nm,layout): #requires trimmomatic module | also returns name of trimmed FASTQ file
	import os
	if layout == "single":
		adapter_seqs = "all_SE_adapters.fa"
	elif layout == "paired":
		adapter_seqs = "all_PE_adapters.fa"
	os.system("java -jar /share/apps/Trimmomatic/0.33/trimmomatic-0.33.jar SE %s %s.trimmed ILLUMINACLIP:/home/lloyd/1_projects/2_poaceae_intergenic_transcription/2_genome_size_vs_ig_space/4_Illumina_adapters/%s:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:20 MINLEN:20"%(fastq_nm,fastq_nm,adapter_seqs))
	return fastq_nm+".trimmed"

def run_trimmomatic_hpcc(fastq_nm,layout): #requires Trimmomatic module | also returns name of trimmed FASTQ file
	import os
	if layout == "single":
		adapter_seqs = "all_SE_adapters.fa"
	elif layout == "paired":
		adapter_seqs = "all_PE_adapters.fa"
	os.system("java -jar $TRIM/trimmomatic SE %s %s.trimmed ILLUMINACLIP:/mnt/home/lloydjo1/scripts/A_Small_Read_Processing/Trimming_seqs%s:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:20 MINLEN:20"%(fastq_nm,fastq_nm,adapter_seqs))
	return fastq_nm+".trimmed"

def run_tophat2(processors,min_intron,max_intron,out_dir_nm,bowtie_index,fastq_nm): #requires tophat 2 module
	import os
	os.system("tophat2 -p %s -i %s -I %s -o %s %s %s"%(processors,min_intron,max_intron,out_dir_nm,bowtie_index,fastq_nm))

def merge_bam(out_prefix,bam_files_list): # also returns the merged bam file name
	import os
	out_nm = "%s_merged.bam"%out_prefix
	cmd = "samtools merge %s %s"%(out_nm," ".join(bam_files_list))
	try:
		os.system(cmd)
	except:
		"Command failed, is the SAMTools module loaded?"
	return out_nm

def bam2sam(bam_file): # Module required: SAMTools | also returns sam file name
	import os
	sam_file = bam_file.replace(".bam",".sam")
	try:
		os.system("samtools view -h -o %s %s"%(sam_file,bam_file))
	except:
		"Command failed, is the SAMTools module loaded?"
	return sam_file

def unique_from_sam_tophat(sam_fl): #also returns file name with unique reads
	inp = open(sam_fl)
	unq_out_nm = sam_fl.replace(".sam",".unique.sam")
	out_unq = open(unq_out_nm,"w")
	for line in inp:
		if line.startswith("@"):
			out_unq.write(line)
		else:
			lineLst = line.strip().split("\t")
			flag_value = lineLst[1]
			if flag_value == "0" or flag_value == "16":
				mapq_value = lineLst[4]
				if mapq_value == "50":
					out_unq.write(line)
	out_unq.close()
	inp.close()
	return unq_out_nm

def primary_from_sam_tophat(sam_fl):
	inp = open(sam_fl)
	out_prm = open(sam_fl.replace(".sam",".primary.sam"),"w")
	for line in inp:
		if line.startswith("@"):
			out_prm.write(line)
		else:
			lineLst = line.strip().split("\t")
			flag_value = lineLst[1]
			if flag_value == "0" or flag_value == "16":
				out_prm.write(line)
	out_prm.close()
	inp.close()

def primary_unique_from_sam_tophat(sam_fl):
	inp = open(sam_fl)
	out_prm = open(sam_fl.replace(".sam",".primary.sam"),"w")
	out_unq = open(sam_fl.replace(".sam",".unique.sam"),"w")
	for line in inp:
		if line.startswith("@"):
			out_prm.write(line)
			out_unq.write(line)
		else:
			lineLst = line.strip().split("\t")
			flag_value = lineLst[1]
			if flag_value == "0" or flag_value == "16":
				out_prm.write(line)
				mapq_value = lineLst[4]
				if mapq_value == "50":
					out_unq.write(line)
	out_prm.close()
	out_unq.close()
	inp.close()

def subsample_sam(sam,sample_count): #also returns subsampled sam file name
	inp = open(sam)
	ind_s = ""
	ind = 0
	hdr_l = []
	for line in inp:
		if line.startswith("@"):
			hdr_l.append(line)
		else:
			if ind_s == "":
				ind_s = ind
		ind += 1
	inp.close()
	ind_e = ind
	
	if sample_count[-1].upper() == "M":
		samps = int(sample_count[0:-1])*1000000
	elif sample_count[-1].upper() == "K":
		samps = int(sample_count[0:-1])*1000
	else:
		samps = int(sample_count)
	
	inp = open(sam)
	subsamp_sam_nm = "%s.%s.random"%(sam,sample_count)
	out = open(subsamp_sam_nm,"w")
	read_cnt = ind_e-ind_s
	print read_cnt,ind_e,ind_s 
	import random
	if samps > read_cnt:
		for line in inp:
			out.write(line)
	else:
		for item in hdr_l:
			out.write(item)
		
		ind_list = range(ind_s,ind_e)
		subsamp = random.sample(ind_list,samps)
		subsamp.sort()
		
		line_ind_list = generate_line_indices(sam)
		for i in subsamp:
			inp.seek(line_ind_list[i])
			ln = inp.readline()
			out.write(ln)
	out.close()
	inp.close()
	return subsamp_sam_nm

def sam2txfrag(sam,min_intron,max_intron,fasta_genome,frag_mean_len): # Module required: cufflinks
	import os
	try:
		cmd = "cufflinks -o %s.txfrag --min-intron-length %s --max-intron-length %s --frag-bias-correct %s --frag-len-mean %s %s"%(sam,min_intron,max_intron,fasta_genome,frag_mean_len,sam)
		print cmd
		os.system(cmd)
	except:
		print "Command failed, is the TopHat2 module loaded?"
###
### MATH FUNCTIONS - require floated values

def calc_aucroc(label_list,score_list,pos_nm=1): # requires scikit, NumPy, and SciPy modules! | pos = 1, neg = 0 in label list
	import numpy as np
	from sklearn import metrics
	y = np.array(label_list)
	scores = np.array(score_list)
	fpr,tpr,thresholds = metrics.roc_curve(y,scores,pos_label=pos_nm)
	roc_auc = metrics.auc(fpr,tpr)
	return roc_auc

def calc_prec_rec_fm(tp,fn,fp,tn): # returns precision,recall,fmeasure
	if float(tp) == 0 and float(fp) == 0:
		prcsn = "NC"
	else:
		prcsn = float(tp)/(float(tp)+float(fp))
	rcll = float(tp)/(float(tp)+float(fn))
	if prcsn == 0 and rcll == 0:
		fms = "NC"
	elif prcsn == "NC":
		fms = "NC"
	else:
		fms = (2*prcsn*rcll)/(prcsn+rcll)
	return prcsn,rcll,fms

def calc_kappa(tp,fn,fp,tn):
	tp = float(tp)
	fn = float(fn)
	fp = float(fp)
	tn = float(tn)
	predictedCorrect = tp+tn
	allPredictions = tp+fn+fp+tn
	class1freq = (tp+fn)/allPredictions
	class2freq = (fp+tn)/allPredictions
	numPredC1 = tp+fp
	numPredC2 = fn+tn
	ranC1cor = numPredC1*class1freq
	ranC2cor = numPredC2*class2freq
	randomCorrect = ranC1cor+ranC2cor
	extraSuccesses = predictedCorrect-randomCorrect
	kappa = extraSuccesses/(allPredictions-randomCorrect)
	return kappa

def calc_FNR(fn,tp):
	fn = float(fn)
	tp = float(tp)
	if fn == 0 and tp == 0:
		fnr = "NC"
	else:
		fnr = (fn/(fn+tp))*100
	return fnr

def calc_FPR(fp,tn):
	fp = float(fp)
	tn = float(tn)
	if fp == 0 and tn == 0:
		fpr = "NC"
	else:
		fpr = (fp/(fp+tn))*100
	return fpr

def calc_performance_for_lists(pos_score_l,neg_score_l): # returns: dict{[threshold]:[prec,recall,fmeas,kappa],[threshold]: ... }
	# thrshs = [0.0]
	# thrsh = 0.01
	# while thrsh < 1:
		# thrsh += 0.01
		# thrshs.append(thrsh)
	
	thrshs = list(set(pos_score_l+neg_score_l))
	thrshs.sort()
	
	d = {}
	for thresh in thrshs:
		tp = 0
		fn = 0
		fp = 0
		tn = 0
		for score in pos_score_l:
			if score >= thresh:
				tp += 1
			else:
				fn += 1
		for score in neg_score_l:
			if score >= thresh:
				fp += 1
			else:
				tn += 1
		fnr = calc_FNR(fn,tp)
		fpr = calc_FPR(fp,tn)
		prc,rcl,fm = calc_prec_rec_fm(tp,fn,fp,tn)
		kppa = calc_kappa(float(tp),float(fn),float(fp),float(tn))
		d[str(thresh)] = [prc,rcl,fm,kppa,fnr,fpr]
	return d

def median(list):
	list.sort()
	if len(list) % 2 == 1:
		med_index = int(len(list)/2.0-0.5)
		return list[med_index]
	else:
		i1 = len(list)/2
		i2 = len(list)/2-1
		return (list[i1]+list[i2])/2.0

def std_dev(list):
	from math import sqrt
	mn = sum(list)/len(list)
	sum_squared_dev = 0
	for val in list:
		dev = val-mn
		sq_dv = dev**2
		sum_squared_dev += sq_dv
	std = sqrt((1.0/len(list))*sum_squared_dev)
	return std

def med_abs_dev(list):
	from math import fabs
	from fn import median
	med = median(list)
	dev_list = []
	for val in list:
		dev = fabs(val-med)
		dev_list.append(dev)
	mad = median(dev_list)
	return mad

def calc_pcc(list1,list2):
	ave1 = sum(list1)/len(list1)
	ave2 = sum(list2)/len(list2)
	n_lst = []
	d1_list = []
	d2_list = []
	for i in range(0,len(list1)):
		wrk1 = (list1[i]-ave1)
		wrk2 = (list2[i]-ave2)
		n_lst.append(wrk1*wrk2)
		d1_list.append(wrk1**2)
		d2_list.append(wrk2**2)
	from math import sqrt
	pcc = sum(n_lst)/(sqrt(sum(d1_list))*sqrt(sum(d2_list)))
	return pcc

def rpy_corr(list1,list2,corr_method):
	import rpy2.robjects as robjects
	vec1 = robjects.FloatVector(list1)
	vec2 = robjects.FloatVector(list2)
	corr = robjects.r('cor(%s,%s,method="%s")' % (vec1.r_repr(),\
vec2.r_repr(),corr_method))[0]
	return corr

def factorial(integer):
	if integer == 0:
		factorial = 1
	else:
		vals = range(1,integer+1)
		factorial = 1
		for val in vals:
			factorial = factorial*val
	return factorial

def binomial_prob(n,k,p):
	from fn import factorial
	n_fact = float(factorial(n))
	k_fact = float(factorial(k))
	nk_fact = float(factorial(n-k))
	nOVk = n_fact/(k_fact*nk_fact)
	prob = nOVk*(p**k)*((1-p)**(n-k))
	return prob
