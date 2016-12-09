#P263页,层次聚类
from queue import PriorityQueue
import math
"""
Example code for hierarchical clustering
"""
def getMedian(alist):
    """get median value of list alist"""
    tmp = list(alist)
    tmp.sort()
    alen = len(tmp)
    if (alen % 2) == 1:
        return tmp[alen // 2]
    else:
        return (tmp[alen // 2] + tmp[(alen // 2) - 1]) / 2
def normalizeColumn(column):
    """Normalize column using Modified Standard Score"""
    median = getMedian(column)
    asd = sum([abs(x - median) for x in column]) / len(column)
    result = [(x - median) / asd for x in column]
    return result
class hClusterer:
    """ this clusterer assumes that the first column of the data is a label
    not used in the clustering. The other columns contain numeric data"""
    #参数1:csv文件名
    def __init__(self, filename):
        file = open(filename)
        self.data = {}
        self.counter = 0
        self.queue = PriorityQueue()
        #############################
        ### 读取文件所有内容
        lines = file.readlines()
        file.close()
        header = lines[0].split(',') #获取标题,格式:['列1','列2',...]
        self.cols = len(header) #获取列数目
        self.data = [[] for i in range(len(header))] #根据列长度初始化数据格式:[[],[],[]]
        for line in lines[1:]: #读取数据
            cells = line.split(',') #行元素列表
            toggle = 0 #切换开关
            for cell in range(self.cols):
                if toggle == 0: #获取名称
                   self.data[cell].append(cells[cell])
                   toggle = 1 #切换到获取属性
                else:
                    self.data[cell].append(float(cells[cell])) #获取属性,转浮点格式
        # now normalize number columns (that is, skip the first column)
        #从第二列开始对各数据归一化
        #归一化后self.data格式为:[['列1名称1','列1名称2',...],['列2属性1','列2属性2',...],['列3属性1','列3属性2',...]]
        for i in range(1, self.cols):
                self.data[i] = normalizeColumn(self.data[i])
        ###
        ###  I have read in the data and normalized the
        ###  columns. Now for each element i in the data, I am going to
        ###     1. compute the Euclidean Distance from element i to all the
        ###        other elements.  This data will be placed in neighbors,
        ###        which is a Python dictionary. Let's say i = 1, and I am
        ###        computing the distance to the neighbor j and let's say j
        ###        is 2. The neighbors dictionary for i will look like
        ###        {2: ((1,2), 1.23),  3: ((1, 3), 2.3)... }
        ###
        ###     2. find the closest neighbor
        ###
        ###     3. place the element on a priority queue, called simply queue,
        ###        based on the distance to the nearest neighbor (and a counter
        ###        used to break ties.
        # now push distances on queue
        rows = len(self.data[0]) #获取数据行数
        for i in range(rows):
            minDistance = 99999 #初始化最小距离
            nearestNeighbor = 0 #初始化最近邻个数
            neighbors = {} #初始化最近邻字典
            for j in range(rows):
                if i != j: #自己不和自己计算距离
                    dist = self.distance(i, j) #计算两个用户的距离
                    #将i,j两用户配对
                    if i < j:
                        pair = (i,j)
                    else:
                        pair = (j,i)
                    neighbors[j] = (pair, dist) #格式:{用户1:((用户0,用户1),距离), 用户2:((用户0,用户2),距离)}
                    #计算出于用户i最小距离的用户j的序号,并记录最小距离值
                    if dist < minDistance:
                        minDistance = dist
                        nearestNeighbor = j
                        nearestNum = j #<--此句已无效
            # create nearest Pair
            #创建最小距离的配对:针对单个用户i
            if i < nearestNeighbor:
                nearestPair = (i, nearestNeighbor)
            else:
                nearestPair = (nearestNeighbor, i)
            # put instance on priority queue
            #队列输入self.queue
            #格式:[(最小距离,用户计数,[['用户名'],(最小配对),{与所有非己用户的配对距离})]
            self.queue.put((minDistance, self.counter,
                            [[self.data[0][i]], nearestPair, neighbors]))
            self.counter += 1 #用户计数器加1
    #############################
    ### 计算两个用户的距离
    ### 欧式距离
    def distance(self, i, j):
        sumSquares = 0
        for k in range(1, self.cols):
            sumSquares += (self.data[k][i] - self.data[k][j])**2
        return math.sqrt(sumSquares)
    ###
    #############################
    def cluster(self):
         done = False
         while not done:
             topOne = self.queue.get()
             nearestPair = topOne[2][1]
             if not self.queue.empty():
                 nextOne = self.queue.get()
                 nearPair = nextOne[2][1] #获取配对(i,j)
                 tmp = []
                 ##
                 ##  I have just popped two elements off the queue,
                 ##  topOne and nextOne. I need to check whether nextOne
                 ##  is topOne's nearest neighbor and vice versa.
                 ##  If not, I will pop another element off the queue
                 ##  until I find topOne's nearest neighbor. That is what
                 ##  this while loop does.
                 ##  针对非对称情况下的处理方式
                 while nearPair != nearestPair:
                     tmp.append((nextOne[0], self.counter, nextOne[2]))
                     self.counter += 1
                     nextOne = self.queue.get()
                     nearPair = nextOne[2][1]
                 ##
                 ## this for loop pushes the elements I popped off in the
                 ## above while loop.
                 ##
                 for item in tmp:
                     self.queue.put(item)
                 if len(topOne[2][0]) == 1:
                    item1 = topOne[2][0][0]
                 else:
                     item1 = topOne[2][0]
                 if len(nextOne[2][0]) == 1:
                    item2 = nextOne[2][0][0]
                 else:
                     item2 = nextOne[2][0]
                 ##  curCluster is, perhaps obviously, the new cluster
                 ##  which combines cluster item1 with cluster item2.
                 curCluster = (item1, item2) #输出合并后的分类
                 ## Now I am doing two things. First, finding the nearest
                 ## neighbor to this new cluster. Second, building a new
                 ## neighbors list by merging the neighbors lists of item1
                 ## and item2. If the distance between item1 and element 23
                 ## is 2 and the distance betweeen item2 and element 23 is 4
                 ## the distance between element 23 and the new cluster will
                 ## be 2 (i.e., the shortest distance).
                 ##
                 minDistance = 99999
                 nearestPair = ()
                 nearestNeighbor = ''
                 merged = {}
                 nNeighbors = nextOne[2][2]
                 #############################
                 ### 此处的代码是层次聚类的核心
                 for (key, value) in topOne[2][2].items(): #key和value分别是最短配对和距离
                    if key in nNeighbors:
                        if nNeighbors[key][1] < value[1]:
                             dist =  nNeighbors[key]
                        else:
                            dist = value
                        if dist[1] < minDistance:
                             minDistance =  dist[1]
                             nearestPair = dist[0]
                             nearestNeighbor = key
                        merged[key] = dist #创造了合并后的新数据并重新记录进merged
                 ###
                 #此部分计算完成后,merge内保存所有用户i的最近邻用户j
                 #格式:{用户1:((1,J1),距离1), 用户2:((2,J2),距离2),...}
                 #############################
                 if merged == {}:
                    return curCluster
                 else:
                    self.queue.put( (minDistance, self.counter,
                                     [curCluster, nearestPair, merged]))
                    self.counter += 1
def printDendrogram(T, sep=3):
    """Print dendrogram of a binary tree.  Each tree node is represented by a
    length-2 tuple. printDendrogram is written and provided by David Eppstein
    2002. Accessed on 14 April 2014:
    http://code.activestate.com/recipes/139422-dendrogram-drawing/ """
    def isPair(T):
        return type(T) == tuple and len(T) == 2
    def maxHeight(T):
        if isPair(T):
            h = max(maxHeight(T[0]), maxHeight(T[1]))
        else:
            h = len(str(T))
        return h + sep
    activeLevels = {}
    def traverse(T, h, isFirst):
        if isPair(T):
            traverse(T[0], h-sep, 1)
            s = [' ']*(h-sep)
            s.append('|')
        else:
            s = list(str(T))
            s.append(' ')
        while len(s) < h:
            s.append('-')
        if (isFirst >= 0):
            s.append('+')
            if isFirst:
                activeLevels[h] = 1
            else:
                del activeLevels[h]
        A = list(activeLevels)
        A.sort()
        for L in A:
            if len(s) < L:
                while len(s) < L:
                    s.append(' ')
                s.append('|')
        print (''.join(s))
        if isPair(T):
            traverse(T[1], h-sep, 0)
    traverse(T, maxHeight(T), -1)
#filename = 'cereal.csv' #<--该实验P279页
filename = 'dogs.csv'
hg = hClusterer(filename)
cluster = hg.cluster()
printDendrogram(cluster)
