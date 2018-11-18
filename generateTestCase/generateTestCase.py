import numpy as np


def generateMatrix(row, col):
    mat = np.random.randint(2, size=(row, col + 1))
    mat[:, 0] = np.arange(1, row + 1)
    return mat


rows = [i * 10000 for i in [1, 10, 100,1000]]
columns = [10, 20, 30, 40]
for row in rows:
    for col in columns:
        np.savetxt(str(row) + "_" + str(col) + ".txt", generateMatrix(row, col), fmt="%d")
        print str(row)+"_"+str(col)+".txt"
