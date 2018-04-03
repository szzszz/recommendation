from numpy import *
from numpy import linalg as la

def loadExData():
    return[[1, 1, 1, 0, 0],
            [2, 2, 2, 0, 0],
            [1, 1, 1, 0, 0],
            [5, 5, 5, 0, 0],
            [1, 1, 0, 2, 2],
            [0, 0, 0, 3, 3],
            [0, 0, 0, 1, 1]]

def loadExData3():
    return[[4, 4, 0, 2, 2],
            [4, 0, 0, 3, 3],
            [4, 0, 0, 1, 1],
            [1, 1, 1, 2, 0],
            [2, 2, 2, 0, 0],
            [1, 1, 1, 0, 0],
            [5, 5, 5, 0, 0]]

def loadExData2():
    return[[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
           [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
           [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
           [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
           [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
           [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
           [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
           [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
           [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
           [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
           [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]

def ecludSim(inA,inB):
    return 1.0/(1.0 + la.norm(inA - inB))

def pearsSim(inA,inB):
    if len(inA) < 3 : return 1.0
    return 0.5+0.5*corrcoef(inA, inB, rowvar = 0)[0][1]
  
def cosSim(inA,inB):
    num = float(inA.T*inB)
    denom = la.norm(inA)*la.norm(inB)
    return 0.5+0.5*(num/denom)

#计算在给定相似度计算方法的条件下，用户对物品的估计评分值
#standEst()函数中：参数dataMat表示数据矩阵，user表示用户编号，simMeas表示相似度计算方法，item表示物品编号  
def standEst(dataMat,user,simMeas,item):
    n=shape(dataMat)[1] #shape用于求矩阵的行列  
    simTotal=0.0; ratSimTotal=0.0
    for j in range(n):
        userRating=dataMat[user,j]
        if userRating==0:continue #若某个物品评分值为0，表示用户未对物品评分，则跳过，继续遍历下一个物品  
        #寻找两个用户都评分的物品  
        overLap=nonzero(logical_and(dataMat[:,item].A>0,dataMat[:,j].A>0))[0]

        if len(overLap)==0:similarity=0  
        else: similarity=simMeas(dataMat[overLap,item],dataMat[overLap,j])

        #print'the %d and %d similarity is: %f' %(item,j,similarity)
        #根据评分来计算相似度，乘以userrating是为了扩大相似度，增加差异
        simTotal+=similarity
        ratSimTotal+=similarity*userRating
    if simTotal==0: return 0
    else: return ratSimTotal/simTotal9

def recommend(dataMat,user,N=3,simMeas=cosSim,estMethod=standEst):
    #寻找未评级的物品  
    #返回第user行等于0的列下标 
    unratedItems = nonzero(dataMat[user,:].A==0)[1]
    if len(unratedItems) == 0: return 'you rated everything'
    itemScores = []
    for item in unratedItems:
        estimatedScore=estMethod(dataMat,user,simMeas,item)#对每一个未评分物品，调用standEst()来产生该物品的预测得分  
        itemScores.append((item,estimatedScore))#该物品的编号和估计得分值放入一个元素列表itemScores中  
    #对itemScores进行从大到小排序，返回前N个未评分物品  reverse=True降序 reverse=False升序
    return sorted(itemScores,key=lambda jj:jj[1],reverse=True)[:N]


if __name__ == '__main__':
    myMat = mat(loadExData2())
    print(recommend(myMat, 3, estMethod=svdEst))
