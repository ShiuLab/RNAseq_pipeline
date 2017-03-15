#loops through tophat files, finds those with low mapping percentage

import os, sys

start_dir= sys.argv[1]

D={}
def clear_spaces(string): #returns tab-delimited
	string = string.strip()
	while "  " in string:
		string = string.replace("  "," ")
	string = string.replace(" ","\t")
	return string
	
def add_data_to_dict(inp,filename,D):
    for line in inp:
        line = clear_spaces(line)
        L= line.strip().split("\t")
        percent = "not found"
        percent2 = "not found"
        for x in L:
            if x == "overall":
               percent= L[0]
               print filename, percent
               percent_final = float(percent.split("%")[0])
               #print (percent_final)
               if percent_final >= 80:
                   pass
               else:
                   D[filename]=str(percent_final)  
            if x == "concordant":
                percent2 = L[0]
                #print "concordant pairs", percent2 #not sure if we need to do anything about this percentage/threshold?
                print filename, "concordant", percent2
                

for dir in os.listdir(start_dir):
    if dir.endswith("_tophat"):
        dir2 = start_dir + "/" + dir
        filename = dir.split("_tophat")[0]
        for file in os.listdir(dir2):
            if file == "align_summary.txt":
                inp = open(dir2 + "/" + file)
                #print (inp)
                add_data_to_dict(inp,filename,D)
                inp.close()
                
output = open("bad_mapping_files_checkQC.txt", "w")
for i in D:
    data = D[i]
    output.write('%s\t%s\n' %(i, data))
    
output.close()
