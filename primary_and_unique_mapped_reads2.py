
def print_help():
	print('''
inp1 = SAM file
inp2 = 0 for SE, 1 for PE
''')

def write_primary_unique(sam_fl, in2):
	inp = open(sam_fl)
	if in2 == 0:
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
	   			
	if in2 == 1:
	   out_unq = open(sam_fl.replace(".sam",".unique.sam"),"w")
	   for line in inp:
	       if line.startswith("@"):
	           out_unq.write(line)
	       else:
	           lineLst = line.strip().split("\t")
	           flag_value_list= [0,4,8,16,73,89,137,153]
	           flag_value = int(lineLst[1])
	           if flag_value in flag_value_list:
	               pass
	           else:
	               mapq_value = lineLst[4]
	               if mapq_value == "50":
	                   out_unq.write(line)
	               else:
	                   pass
	   out_unq.close()
	else:
	    print ("not SE or PE", inp)    
	
	inp.close()

def main():
	import sys
	if len(sys.argv) == 1 or "-h" in sys.argv:
		print_help()
		sys.exit()
	
	try:
		sam_file = sys.argv[1]
		inp2 = int(sys.argv[2])
	except:
		print_help()
		print ("Error reading arguments, quitting!")
		sys.exit()
	
	write_primary_unique(sam_file, inp2)

if __name__ == "__main__":
	main()
