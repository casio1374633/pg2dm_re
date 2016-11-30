#
#  Classify Template
#
#  Finish the code for the method, nearestNeighbor
#
#  Code file for the book Programmer's Guide to Data Mining
#  http://guidetodatamining.com
#
#  Ron Zacharski
#
#分类器训练模块类
class Classifier:
    #传递训练数据
    def __init__(self, filename):
        self.medianAndDeviation = [] #deviation:偏差
        # reading the data in from the file
        f = open(filename)
        lines = f.readlines()
        f.close()
        #第一行是标题,一共四个属性,<<comment:注释 class:分类 num:属性1 num:属性2>>
        #self.format存放属性列表
        self.format = lines[0].strip().split('\t')
        self.data = [] #存放单条完整的格式化数据
        for line in lines[1:]:
            fields = line.strip().split('\t')
            ignore = [] #存放注释,格式:[注释]
            vector = [] #存放属性,格式:[属性1,属性2]
            for i in range(len(fields)): #按照fields 列项目对比
                if self.format[i] == 'num':
                    vector.append(int(fields[i]))
                elif self.format[i] == 'comment':
                    ignore.append(fields[i])
                elif self.format[i] == 'class':
                    classification = fields[i] #定义一个临时变量存放分类,字符串类型
            self.data.append((classification, vector, ignore)) #格式为:('分类字符串', [属性1,属性2], 注释)
        #print(self.data)
        #self.rawData全文其他地方再没有使用该数据
        self.rawData = list(self.data)
        #print(self.rawData) #通过list(self.data) == (self.data),返回的是True,说明二者相同
        # get length of instance vector
        self.vlen = len(self.data[0][1]) #self.data[0][1] 获取属性列表[属性1,属性2]
        # now normalize the data
        #归一化操作,结果是每个属性值都改为"改进的标准分数",公式在书P109
        for i in range(self.vlen):
            self.normalizeColumn(i)

    ##################################################
    ###
    ###  CODE TO COMPUTE THE MODIFIED STANDARD SCORE
    #alist是列表,一串数
    def getMedian(self, alist):
        """return median of alist"""
        if alist == []:
            return []
        #对列表排序
        blist = sorted(alist)
        length = len(alist)
        #判断奇偶
        if length % 2 == 1:
            #如果是奇数,则返回中间值
            # length of list is odd so return middle element
            return blist[int(((length + 1) / 2) -  1)]
        else:
            #如果是偶数,返回中间两个值得平均值
            # length of list is even so compute midpoint
            v1 = blist[int(length / 2)]
            v2 =blist[(int(length / 2) - 1)]
            return (v1 + v2) / 2.0

    #计算绝对标准差
    def getAbsoluteStandardDeviation(self, alist, median):
        """given alist and median return absolute standard deviation"""
        sum = 0
        for item in alist:
            sum += abs(item - median) #sum(x_i - 中位数)
        return sum / len(alist) #sum / 个数 = 绝对标准差

    #归一化操作,输入参数是列号
    def normalizeColumn(self, columnNumber):
        """given a column number, normalize that column in self.data"""
        # first extract values to list
        #col是列表,存放的是全部self.data的属性i的列值
        col = [v[1][columnNumber] for v in self.data] #v为self.data按行读取,v[1][columnNumber]获取属性列表中的第i列数值
        #获取中位数值(排序中的中间值)
        median = self.getMedian(col)
        #计算asd,在书P109页有公式"绝对标准差"
        asd = self.getAbsoluteStandardDeviation(col, median)
        #print("Median: %f   ASD = %f" % (median, asd))
        #medianAndDeviation存放中位数和绝对标准差,格式为元祖:(中位数,绝对标准差)
        #整个medianAndDeviation为列表,每个单元是元祖.[(中位数1,绝对标准差1), (中位数2, 绝对标准差2)]
        self.medianAndDeviation.append((median, asd))
        #计算属性i的每个数值的改进标准分数
        for v in self.data:
            #公式在P109页,"(每个值 - 中位数) / 绝对标准差 = 改进的标准分数"
            v[1][columnNumber] = (v[1][columnNumber] - median) / asd

    #对待测用户的属性归一化
    def normalizeVector(self, v):
        """We have stored the median and asd for each column.
        We now use them to normalize vector v"""
        #list(v)和v是一致的,v本身就是列表
        vector = list(v)
        for i in range(len(vector)):
            #获取对应属性的(中位数,绝对标准差)
            (median, asd) = self.medianAndDeviation[i]
            #归一化对应属性的数值
            vector[i] = (vector[i] - median) / asd
        return vector
    ###
    ### END NORMALIZATION
    ##################################################

    #计算曼哈顿距离
    def manhattan(self, vector1, vector2):
        """Computes the Manhattan distance."""
        return sum(map(lambda v1, v2: abs(v1 - v2), vector1, vector2))


    #def nearestNeighbor(self, itemVector):
    #    """return nearest neighbor to itemVector"""
    #    return ((0, ("REPLACE THIS LINE WITH CORRECT RETURN", [0], [])))
    #输入为待测用户的属性列表
    def nearestNeighbor(self, itemVector):
        """return nearest neighbor to itemVector"""
        #对该属性计算每个用户和他的曼哈顿距离,并输出最小值
        #格式为:[(用户1的属性列表,(分类,[属性列表],注释)), (用户2的属性列表,(分类,[属性列表],注释))]
        return min([ (self.manhattan(itemVector, item[1]), item) #此处item为data的一行,item[1]获取属性列表
                     for item in self.data])
    #输出计算出来的最小邻近的分类结果
    def classify(self, itemVector):
        """Return class we think item Vector is in"""
        return(self.nearestNeighbor(self.normalizeVector(itemVector))[1][0]) #根据上面的格式,得知获取item中的分类字符串

def unitTest():
    #初始化训练数据:读取文件,归一化
    classifier = Classifier('./dataset/athletesTrainingSet.txt')
    #待测用户三个
    br = ('Basketball', [72, 162], ['Brittainey Raven'])
    nl = ('Gymnastics', [61, 76], ['Viktoria Komova'])
    cl = ("Basketball", [74, 190], ['Crystal Langhorne'])
    # first check normalize function
    #待测用户的属性归一化
    brNorm = classifier.normalizeVector(br[1])
    nlNorm = classifier.normalizeVector(nl[1])
    clNorm = classifier.normalizeVector(cl[1])
    #测试对比归一化结果是否正确
    #brNorm只有归一化的属性列表[属性1,属性2]
    assert(brNorm == classifier.data[1][1]) #对比train文件第二个用户
    assert(nlNorm == classifier.data[-1][1]) #对比train文件倒数第一个用户
    print('normalizeVector fn OK')
    # check distance
    #测试距离,确保距离计算结果正确
    assert (round(classifier.manhattan(clNorm, classifier.data[1][1]), 5) == 1.16823)
    assert(classifier.manhattan(brNorm, classifier.data[1][1]) == 0)
    assert(classifier.manhattan(nlNorm, classifier.data[-1][1]) == 0)
    print('Manhattan distance fn OK')
    # Brittainey Raven's nearest neighbor should be herself
    result = classifier.nearestNeighbor(brNorm)
    try:
       assert(result[1][2]== br[2])
    finally:
       print(result[1][2], br[2])

    # Nastia Liukin's nearest neighbor should be herself
    result = classifier.nearestNeighbor(nlNorm)
    try:
       assert(result[1][2]== nl[2])
    finally:
       print(result[1][2], nl[2])

    # Crystal Langhorne's nearest neighbor is Jennifer Lacy"
    try:
       assert(classifier.nearestNeighbor(clNorm)[1][2][0] == "Jennifer Lacy")
    finally:
       print(classifier.nearestNeighbor(clNorm)[1][2][0])

    print("Nearest Neighbor fn OK")
    # Check if classify correctly identifies sports
    assert(classifier.classify(br[1]) == 'Basketball')
    assert(classifier.classify(cl[1]) == 'Basketball')
    assert(classifier.classify(nl[1]) == 'Gymnastics')
    print('Classify fn OK')

if __name__ == "__main__":
   unitTest()
