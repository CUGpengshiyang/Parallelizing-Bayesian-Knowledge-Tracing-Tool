import os 
line = ["1w","10w","100w"]
col = ["50","60","70"]
for i in range(len(line)):
	for j in range(len(col)):
		appId = "%03d"%(6+i*len(line)+j)
		objFile = "3_"+line[i]+"_"+col[j]+".txt"
		os.system("yarn logs -applicationId application_1507707882762_0"+appId+" > "+objFile)
