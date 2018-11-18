import os 
files = os.listdir(".")
for file in filter(lambda x:x.endswith(".txt"),files):
	file_name = file.split(".")[0]
	lines = open(file,"r").readlines()
	index = 0
	tempfile = open("temp","w")
	while "python my HMM" not in lines[index]:
		index+=1
	while "hmm.pi" not in lines[index]:
		tempfile.write(lines[index])
		index+=1
	tempfile.write(lines[index])
	tempfile.write(lines[index+1])
	tempfile.write(lines[index+2])
	tempfile.write(lines[index+3])
	tempfile.write(lines[index+4])
	tempfile.close()
	os.system("mv temp "+file)
