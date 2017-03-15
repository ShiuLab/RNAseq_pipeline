# IMPORT
import os,sys

# MAIN
print('''
inp1 = GFF file for gene-id conversions 
inp2 = alternative splicings which should be neglected
inp3 = directory for cufflinks or htseq outputs
inp4 = cufflink data (c) or htseq data (h)
inp5 = threshold value of FPKM_conf_lo
inp6 = Sample name file
examples:
	Cufflink:
		python Combine_info_cuffhtseq.py /mnt/home/peipeiw/Documents/Pathway_prediction/Mapping/Solanum_lycopersicum_GCF_000188115.3_S.lycopersicum.2.50_genomic.gff /mnt/home/peipeiw/Documents/Pathway_prediction/Mapping/Solanum_lycopersicum_GCF__gene_get_rid_of.txt ./cufflink_results/ c 0 /mnt/home/peipeiw/Documents/Pathway_prediction/Mapping/Sample_name.txt
	Htseq:
		python Combine_info_cuffhtseq.py /mnt/home/peipeiw/Documents/Pathway_prediction/Mapping/Solanum_lycopersicum_GCF_000188115.3_S.lycopersicum.2.50_genomic.gff /mnt/home/peipeiw/Documents/Pathway_prediction/Mapping/Solanum_lycopersicum_GCF__gene_get_rid_of.txt htseq_results/ h 0 /mnt/home/peipeiw/Documents/Pathway_prediction/Mapping/Sample_name.txt
''')

#directory for rna-id --> gene-id
R = {}
#directory for protein-id --> rna-id
P = {}
#directory for gene-id --> protein-id
G = {}
#directory of gene list of alternative splicing
L = {}
#directory saving the finally result of cufflink
C = {}
#directory saving the finally result of htseq
H = {}
#directory for SRR id --> sample name
S = {}

#get the gene list of alternative splicing
inp = open(sys.argv[2],'r').readlines()
for inl in inp:
	tem = inl.split('\t')
	L[tem[0]] = 1

#get gene info from gff file
gop = open(sys.argv[1],"r")
line = gop.readline()
while line:
	if line.startswith("#"):
		pass
	else:
		info = line.strip().split("\t")
		if info[2] == "mRNA":
			# inform = info[8].split(";")
			# for j in inform:
				# if j.startswith("Parent"):
					# geneid = j.split("=")[1]
				# if j.startswith("Genbank"):
					# genecode = j.split(":")[1]
			rna = info[8].split(";")[0].split('ID=')[1]
			rnaparent = info[8].split(";")[1].split('Parent=')[1]
			R[rna] = rnaparent
		if info[2] == "CDS":
			cds = info[8].strip().split("protein_id=")[1].split(';')[0]
			cdsparent = info[8].split(";")[1].split('Parent=')[1]
			if cds not in P and cds not in L:
				P[cds] = cdsparent
	line = gop.readline()

for cds in P:
	if P[cds].startswith('rna'):
		gene = R[P[cds]]
		G[gene] = cds
	if P[cds].startswith('gene'):
		gene = P[cds]
		G[gene] = cds

sample = open('Sample_name.txt','r').readlines()
for s in sample:
	tem = s.strip().split('\t')
	S[tem[1]] = tem[0]

cutoff = int(sys.argv[5])
samplelist = []
#parse the cufflink results
if sys.argv[4] == 'c':
	for files in os.listdir(sys.argv[3]):
		if files.endswith('_genes.fpkm_tracking'):
			sample = files.split('_genes.fpkm_tracking')[0]
			samplelist.append(sample)
			dat = open(sys.argv[3] + files,'r')
			l = dat.readline()
			l = dat.readline()
			while l != '':
				lin = l.split('\t')
				if lin[3] in G:
					if G[lin[3]] not in C:
						C[G[lin[3]]] = {}
					if(float(lin[10]) > cutoff):
						C[G[lin[3]]][sample] = float(lin[9])
					else:
						C[G[lin[3]]][sample] = 0
				l = dat.readline()
	oup1 = open('Cufflink_matrix.txt','w')
	oup1s = open('Cufflink_matrix_sample_name.txt','w')
	title = 'gene'
	titles = 'gene'
	for sample in sorted(samplelist):
		title = title  + '\t' + sample
		titles = titles  + '\t' + S[sample]
	#write the title
	oup1.write(title + '\n')
	oup1s.write(titles + '\n')
	#write the results of cufflink
	for gene in C:
		res = gene
		for sample in sorted(samplelist):
			res = res + '\t' + '%s'%(C[gene][sample])
		oup1.write(res + '\n')
		oup1s.write(res + '\n')
	oup1.close()
	oup1s.close()

else:
	for files in os.listdir(sys.argv[3]):
		if files.endswith('_htseq_counts') or files.endswith('_uniquecounts'):
			sample = files.split('_htseq')[0]
			samplelist.append(sample)
			dat = open(sys.argv[3] + files,'r')
			l = dat.readline()
			while l != '':
				if not l.startswith('__'):
					lin = l.strip().split('\t')
					if lin[0] in G:
						if G[lin[0]] not in H:
							H[G[lin[0]]] = {}
						H[G[lin[0]]][sample] = int(lin[1])
				l = dat.readline()
	oup2 = open('HTseq_matrix.txt','w')
	oup2s = open('HTseq_matrix_sample_name.txt','w')
	title = 'gene'
	titles = 'gene'
	for sample in sorted(samplelist):
		title = title  + '\t' + sample
		titles = titles  + '\t' + S[sample]
	#write the title
	oup2.write(title + '\n')
	oup2s.write(titles + '\n')
	#write the results of HTseq
	for gene in H:
		res = gene
		for sample in sorted(samplelist):
			if sample in H[gene].keys():
				res = res + '\t' + '%s'%(H[gene][sample])
			else:
				res = res + '\tNa'
		oup2.write(res + '\n')
		oup2s.write(res + '\n')
	oup2.close()
	oup2s.close()
















