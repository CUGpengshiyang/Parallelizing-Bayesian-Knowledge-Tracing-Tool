import os 
line = ["10w","100w"]
col = ["50","60"]
for i in range(len(line)):
	for j in range(len(col)):
		appId = 181+i*len(line)+j
		objFile = "5_"+line[i]+"_"+col[j]+".txt"
		os.system("yarn logs -applicationId application_1507280810513_0"+str(appId)+" > "+objFile)
