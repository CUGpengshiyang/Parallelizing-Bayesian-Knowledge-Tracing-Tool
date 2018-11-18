import numpy as np


Pt = [0.2, 0.15, 0.1, 0.05]
Pg = [0.2, 0.15, 0.1, 0.05]
Ps = [0.05, 0.1, 0.15, 0.2]


def getSequence(mat, row, cols,index):
    P_T = Pt[index]
    P_G = Pg[index]
    P_S = Ps[index]
    stats = 0.2
    prob =stats*(1-P_S)+(1-stats)*P_G
    knowledge_pro = [stats for i in range(1+cols)]
    randoms = np.random.random((1,cols))
    for i in range(cols):
        if randoms[0,i]< knowledge_pro[i]:
            mat[row, i + 1] = 1
            stats = stats * (1 - P_S) / (stats * (1 - P_S) + (1 - stats) * P_G)
        else:
            mat[row, i + 1] = 0
            stats = stats * P_S / (stats * P_S + (1 - stats) * (1 - P_G))
        stats = stats + (1 - stats) * P_T
        knowledge_pro[i+1] = stats*(1-P_S)+(1-stats)*P_G


def generateMatrix(row, cols):
    mat = np.zeros((row, cols + 1))
    mat[:, 0] = np.arange(1, row + 1)
    for i in range(row):
        getSequence(mat, i, cols, cols // 10 - 1)
    return mat


rows = [i * 10000 for i in [1,10,100]]
columns = [10,20,30,40]
for row in rows:
    for col in columns:
        np.savetxt(str(row) + "_" + str(col) + ".txt",
                   generateMatrix(row, col), fmt="%d")
        print str(row) + "_" + str(col) + ".txt"
