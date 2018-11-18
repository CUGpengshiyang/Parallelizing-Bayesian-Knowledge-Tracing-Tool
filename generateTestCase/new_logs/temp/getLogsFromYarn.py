import os 
line = ["1w","10w","100w"]
col = ["10","20","30"]
index = 0
for i in range(9):
    for j in range(9):
        appId = "%03d"%(200+index)
        index+=1
        objFile = str(i+1)+str(j+1)+".txt"
        print "yarn logs -applicationId application_1507707882762_0"+appId+" > "+objFile
        os.system("yarn logs -applicationId application_1507707882762_0"+appId+" > "+objFile)
