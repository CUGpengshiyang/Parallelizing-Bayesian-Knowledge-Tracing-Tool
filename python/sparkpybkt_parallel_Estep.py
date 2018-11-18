# -*-coding:UTF-8-*-
import numpy as np
import json
import random
import numpy as np
import pandas as pd
import datetime
import math
from pyspark import SparkContext, SparkConf

starttime = datetime.datetime.now()
appName = "testsp"  # 你的应用程序名称
master = "yarn-cluster"  # 设置单机
conf = SparkConf().setAppName(appName).setMaster(master)  # 配置SparkContext
sc = SparkContext(conf=conf)


# long running

# 函数名称：Forward *功能：前向算法估计参数 *参数:phmm:指向HMM的指针
# T:观察值序列的长度 O:观察值序列
# alpha:运算中用到的临时数组 pprob:返回值,所要求的概率
# 带修正的前向算法
def ForwardWithScale(O, alpha, scale, pprob, N, pi, A, B, lT):
    scale[0] = 0.0
    #     1. Initialization
    for i in range(N):
        alpha[0, i] = pi[i] * B[i, O[0]]
        scale[0] += alpha[0, i]

    for i in range(N):
        alpha[0, i] /= scale[0]

    # 2. Induction
    for t in range(lT - 1):
        scale[t + 1] = 0.0
        for j in range(N):
            sum = 0.0
            for i in range(N):
                sum += alpha[t, i] * A[i, j]

            alpha[t + 1, j] = sum * B[j, O[t + 1]]
            scale[t + 1] += alpha[t + 1, j]
        for j in range(N):
            alpha[t + 1, j] /= scale[t + 1]

            #     3. Termination

    for t in range(T):
        pprob[0] += np.log(scale[t])


def BackwardWithScale(O, beta, scale, N, A, B, lT):
    #     1. Intialization
    for i in range(N):
        beta[lT - 1, i] = 1.0

    # 2. Induction
    for t in range(lT - 2, -1, -1):
        for i in range(N):
            sum = 0.0
            for j in range(N):
                sum += A[i, j] * B[j, O[t + 1]] * beta[t + 1, j]
            beta[t, i] = sum / scale[t + 1]


# 计算gamma : 时刻t时马尔可夫链处于状态Si的概率
def ComputeGamma(alpha, beta, gamma, N):
    for t in range(T):
        denominator = 0.0
        for j in range(N):
            gamma[t, j] = alpha[t, j] * beta[t, j]
            denominator += gamma[t, j]
        for i in range(N):
            gamma[t, i] = gamma[t, i] / denominator


# 计算sai(i,j) 为给定训练序列O和模型lambda时：
# 时刻t是马尔可夫链处于Si状态，二时刻t+1处于Sj状态的概率
def ComputeXi(O, alpha, beta, gamma, xi, N, A, B):
    for t in range(T - 1):
        sum = 0.0
        for i in range(N):
            for j in range(N):
                xi[t, i, j] = alpha[t, i] * beta[t + 1, j] * A[i, j] * B[j, O[t + 1]]
                sum += xi[t, i, j]
        for i in range(N):
            for j in range(N):
                xi[t, i, j] /= sum


# E步骤并行化
def E_Parallel(O, N, M, A, B, lT, lpi):
    result={}
    alpha = np.zeros((lT, N), np.float)
    beta = np.zeros((lT, N), np.float)
    gamma = np.zeros((lT, N), np.float)
    pi = np.zeros((lT), np.float)
    denominatorA = np.zeros((N), np.float)
    denominatorB = np.zeros((N), np.float)
    numeratorA = np.zeros((N, N), np.float)
    numeratorB = np.zeros((N, M), np.float)
    probf = [0.0]
    scale = np.zeros((lT), np.float)
    xi = np.zeros((lT, N, N))
    pi = np.zeros((lT), np.float)
    ForwardWithScale(O, alpha, scale, probf, N, lpi, A, B, lT)
    BackwardWithScale(O, beta, scale, N, A, B, lT)
    ComputeGamma(alpha, beta, gamma, N)
    ComputeXi(O, alpha, beta, gamma, xi, N, A, B)
    for i in range(N):
        pi[i] += gamma[0, i]
        for t in range(lT - 1):
            denominatorA[i] += gamma[t, i]
            denominatorB[i] += gamma[t, i]
        denominatorB[i] += gamma[lT - 1, i]

        for j in range(N):
            for t in range(lT - 1):
                numeratorA[i, j] += xi[t, i, j]
        for k in range(M):
            for t in range(lT):
                if O[t] == k:
                    numeratorB[i, k] += gamma[t, i]

    result['pi'] = pi
    result['denominatorA'] = denominatorA
    result['denominatorB'] = denominatorB
    result['numeratorA'] = numeratorA
    result['numeratorB'] = numeratorB
    result['probf'] = probf[0]
    return result


def E_reduce(x, y, N, M, lT):
    z = {}
    z['probf']=0.0
    pi = np.zeros((lT), np.float)
    denominatorA = np.zeros((N), np.float)
    denominatorB = np.zeros((N), np.float)
    numeratorA = np.zeros((N, N), np.float)
    numeratorB = np.zeros((N, M), np.float)
    z['probf'] = x['probf'] + y['probf']
    for i in range(lT):
        pi[i] = x['pi'][i] + y['pi'][i]
    z['pi']=pi
    for i in range(N):
        denominatorA[i] = x['denominatorA'][i] + y['denominatorA'][i]
        denominatorB[i] = x['denominatorB'][i] + y['denominatorB'][i]
        for j in range(N):
            numeratorA[i][j] = x['numeratorA'][i][j] + y['numeratorA'][i][j]
        for j in range(M):
            numeratorB[i][j] = x['numeratorB'][i][j] + y['numeratorB'][i][j]
    z['denominatorA']=denominatorA
    z['denominatorB']=denominatorB
    z['numeratorA']=numeratorA
    z['numeratorB']=numeratorB
    return z


class HMM:
    def __init__(self, Ann, Bnm, pi1n):
        self.A = np.array(Ann)
        self.B = np.array(Bnm)
        self.pi = np.array(pi1n)
        self.N = self.A.shape[0]
        self.M = self.B.shape[1]

    def printhmm(self):
        print "=================================================="
        print "HMM content: N =", self.N, ",M =", self.M
        for i in range(self.N):
            if i == 0:
                print "hmm.A ", self.A[i, :], " hmm.B ", self.B[i, :]
            else:
                print "      ", self.A[i, :], "       ", self.B[i, :]
        print "hmm.pi", self.pi
        print "=================================================="

    # Baum-Welch算法
    # 输入 L个观察序列O，初始模型：HMM={A,B,pi,N,M}
    def BaumWelch(self, O, alpha, beta, gamma):
        print "BaumWelch"
        DELTA = 0.001;
        round = 0;
        flag = 1;
        probf = 0.0
        delta = 0.0;
        deltaprev = 0.0;
        probprev = 0.0;
        ratio = 0.0;
        deltaprev = 10e-70

        xi = np.zeros((T, self.N, self.N))
        pi = np.zeros((T), np.float)
        denominatorA = np.zeros((self.N), np.float)
        denominatorB = np.zeros((self.N), np.float)
        numeratorA = np.zeros((self.N, self.N), np.float)
        numeratorB = np.zeros((self.N, self.M), np.float)
        scale = np.zeros((T), np.float)

        print "user_num  %s" % L
        while True:
            print "num iteration ", round
            probf = 0
            sumpi = 0
            # E - step
            rddO = sc.parallelize(O)
            N = self.N
            M = self.M
            A = self.A
            B = self.B
            lT = T
            lpi = self.pi
            result = rddO.map(lambda x: E_Parallel(x, N, M, A, B, lT, lpi))
            resultrd = result.reduce(lambda x, y: E_reduce(x, y, N, M, lT))
            pi = resultrd['pi']
            numeratorA = resultrd['numeratorA']
            denominatorA = resultrd['denominatorA']
            denominatorB = resultrd['denominatorB']
            numeratorB = resultrd['numeratorB']
            probf = resultrd['probf']
            print "da:",denominatorB
            print "na:",numeratorB
            # M - step
            # 重估状态转移矩阵 和 观察概率矩阵
            for i in range(self.N):
                self.pi[i] = pi[i] / L
                for j in range(self.N):
                    self.A[i, j] = numeratorA[i, j] / denominatorA[i]
                    numeratorA[i, j] = 0.0

                for k in range(self.M):
                    self.B[i, k] = numeratorB[i, k] / denominatorB[i]
                    numeratorB[i, k] = 0.0

                pi[i] = denominatorA[i] = denominatorB[i] = 0.0;
            print self.A
            print self.B
            print "Pi:",self.pi
            print probf
            if flag == 1:
                flag = 0
                probprev = probf
                ratio = 1
                continue

            delta = probf - probprev
            ratio = delta / deltaprev
            probprev = probf
            deltaprev = delta
            round += 1
            print "rate:", ratio, DELTA
            if ratio <= DELTA:
                print "num iteration ", round
                print "rate:", ratio, DELTA
                break

        self.P_T = self.A[0][1]
        self.P_G = self.B[0][1]
        self.P_S = self.B[1][0]

    def inference(self, priors_info, observations_info):
        knowledge_stats = {}

        for id in observations_info:
            #print '\t\t正在处理 user_id: %s' % str(id)
            knowledge_pro = [0]
            observation = observations_info[id]
            if id in priors_info:
                stats = priors_info[id]
            else:
                stats = 0.5
            knowledge_pro[0] = stats
            for question in observation:
                if question == 1:
                    stats = stats * (1 - self.P_S) / (stats * (1 - self.P_S) + (1 - stats) * self.P_G)
                else:
                    stats = stats * self.P_S / (stats * self.P_S + (1 - stats) * (1 - self.P_G))
                stats = stats + (1 - stats) * self.P_T;
                knowledge_pro.append(stats)
                # stats = self.statss[id]
            knowledge_stats[id] = knowledge_pro

        return knowledge_stats


if __name__ == "__main__":
    print "python my HMM"

    A = [[0.82, 0.18], [0.2, 0.8]]
    B = [[0.875, 0.125], [0.25, 0.75]]
    pi = [0.5, 0.5]
    hmm = HMM(A, B, pi)
    # priors_path = "source_files/HMM/lr_result.json"
    # priors_file = open(priors_path, 'r')
    # priors_info = json.load(priors_file)
    # priors_file.close()
    priors_info = {}
    hdfs_address = 'hdfs://dogs/user/pyj/'
    observations_path = "Q1.txt"
    file = sc.textFile(hdfs_address + observations_path).collect()
    # file = open(observations_path)
    observations_info = {}
    str_list = []

    for line in file:
        i = -1
        num_list = []
        str_list = line.split(" ")
        num_index = 0
        for num in str_list:
            if i == -1:
                num_index = num
                i = i + 1
            else:
                num_list.append(int(num))

        observations_info[num_index] = num_list
    # print observations_info
    # observations_file = open(observations_path, 'r')
    # observations_info = json.load(observations_file)
    # observations_file.close()

    observations = []
    for user in observations_info:
        observations.append(observations_info[user])
    # observations = observations_info-1
    # print observations
    # 训练参数A,B
    global L
    global T
    L = len(observations)  # 学生数量
    T = len(observations[0])  # T等于最长序列的长度就好了
    alpha = np.zeros((T, hmm.N), np.float)
    beta = np.zeros((T, hmm.N), np.float)
    gamma = np.zeros((T, hmm.N), np.float)
    hmm.BaumWelch(observations, alpha, beta, gamma)

    # 根据训练参数预测正确率
    student_result=[]
    inference_result = hmm.inference(priors_info, observations_info)
    endtime = datetime.datetime.now()
    usetime = endtime - starttime
    print 'totaltime:', usetime.seconds
    inference_result['time'] = usetime.seconds
    for i in inference_result:
        student_result.append((i,inference_result[i]))
    data = sc.parallelize(student_result)
    data.saveAsTextFile(hdfs_address + 'result_temp3')
    # dump(inference_result, open("inference1.json", 'w'), indent = 2)
    hmm.printhmm()
