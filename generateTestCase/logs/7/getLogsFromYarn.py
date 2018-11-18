import os 
line = ["1w","10w","100w"]
col = ["10","20","30","40"]
for i in range(3):
	for j in range(4):
		appId = 165+i*4+j
		objFile = "7_"+line[i]+"_"+col[j]+".txt"
		os.system("yarn logs -applicationId application_1507280810513_0"+str(appId)+" > "+objFile)
