import os 
index = 46
line = ["10w","100w"]
col = ["20","30","40"]
for tp in ["16_3g","28_3g","36_2g","48_1g"]:
    for i in range(len(line)):
        for j in range(len(col)):
            appId = "%03d"%(index)
            index+=1
            objFile = tp+"_"+line[i]+"_"+col[j]+".txt"
            print "yarn logs -applicationId application_1507707882762_0"+appId+" > "+objFile
            os.system("yarn logs -applicationId application_1507707882762_0"+appId+" > "+objFile)
