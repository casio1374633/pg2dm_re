#
#  Nearest Neighbor Classifier
#
#
#  Code file for the book Programmer's Guide to Data Mining
#  http://guidetodatamining.com
#
#  Ron Zacharski
#


##   I am trying to make the classifier more general purpose
##   by reading the data from a file.
##   Each line of the file contains tab separated fields.
##   The first line of the file describes how those fields (columns) should
##   be interpreted. The descriptors in the fields of the first line are:
##
##        comment   -  this field should be interpreted as a comment
##        class     -  this field describes the class of the field
##        num       -  this field describes an integer attribute that should
##                     be included in the computation.
##
##        more to be described as needed
##
##
##    So, for example, if our file describes athletes and is of the form:
##    Shavonte Zellous   basketball  70  155
##    The first line might be:
##    comment   class  num   num
##
##    Meaning the first column (name of the player) should be considered a comment;
##    the next column represents the class of the entry (the sport);
##    and the next 2 represent attributes to use in the calculations.
##
##    The classifer reads this file into the list called data.
##    The format of each entry in that list is a tuple
##
##    (class, normalized attribute-list, comment-list)
##
##    so, for example
##
##   [('basketball', [1.28, 1.71], ['Brittainey Raven']),
##    ('basketball', [0.89, 1.47], ['Shavonte Zellous']),
##    ('gymnastics', [-1.68, -0.75], ['Shawn Johnson']),
##    ('gymnastics', [-2.27, -1.2], ['Ksenia Semenova']),
##    ('track', [0.09, -0.06], ['Blake Russell'])]
##

class Classifier:
    def __init__(self, filename):
        self.medianAndDeviation = []
        # reading the data in from the file
        f = open(filename)
        lines = f.readlines()
        f.close()
        self.format = lines[0].strip().split('\t')
        self.data = []
        for line in lines[1:]:
            fields = line.strip().split('\t')
            ignore = []
            vector = []
            for i in range(len(fields)):
                if self.format[i] == 'num':
                    vector.append(float(fields[i]))
                elif self.format[i] == 'comment':
                    ignore.append(fields[i])
                elif self.format[i] == 'class':
                    classification = fields[i]
            self.data.append((classification, vector, ignore))
        self.rawData = list(self.data)
        # get length of instance vector
        self.vlen = len(self.data[0][1])
        # now normalize the data
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
    classifier = Classifier('athletesTrainingSet.txt')
    br = ('Basketball', [72, 162], ['Brittainey Raven'])
    nl = ('Gymnastics', [61, 76], ['Viktoria Komova'])
    cl = ("Basketball", [74, 190], ['Crystal Langhorne'])
    # first check normalize function
    brNorm = classifier.normalizeVector(br[1])
    nlNorm = classifier.normalizeVector(nl[1])
    clNorm = classifier.normalizeVector(cl[1])
    assert(brNorm == classifier.data[1][1])
    assert(nlNorm == classifier.data[-1][1])
    print('normalizeVector fn OK')
    # check distance
    assert (round(classifier.manhattan(clNorm, classifier.data[1][1]), 5) == 1.16823)
    assert(classifier.manhattan(brNorm, classifier.data[1][1]) == 0)
    assert(classifier.manhattan(nlNorm, classifier.data[-1][1]) == 0)
    print('Manhattan distance fn OK')
    # Brittainey Raven's nearest neighbor should be herself
    result = classifier.nearestNeighbor(brNorm)
    assert(result[1][2]== br[2])
    # Nastia Liukin's nearest neighbor should be herself
    result = classifier.nearestNeighbor(nlNorm)
    assert(result[1][2]== nl[2])
    # Crystal Langhorne's nearest neighbor is Jennifer Lacy"
    assert(classifier.nearestNeighbor(clNorm)[1][2][0] == "Jennifer Lacy")
    print("Nearest Neighbor fn OK")
    # Check if classify correctly identifies sports
    assert(classifier.classify(br[1]) == 'Basketball')
    assert(classifier.classify(cl[1]) == 'Basketball')
    assert(classifier.classify(nl[1]) == 'Gymnastics')
    print('Classify fn OK')

#该py适合在python环境下使用import调试,最下面的注释里面有写方式
#可以灵活测试多个不同的数据集
def test(training_filename, test_filename):
    """Test the classifier on a test set of data"""
    #归一化训练数据集
    classifier = Classifier(training_filename)
    ##################################################
    ### 打开测试数据集
    f = open(test_filename)
    lines = f.readlines()
    f.close()
    ###
    ##################################################

    ##################################################
    #计算正确率
    numCorrect = 0.0 #正确个数
    for line in lines:
        data = line.strip().split('\t')
        vector = []
        classInColumn = -1
        for i in range(len(classifier.format)):
              if classifier.format[i] == 'num': #读取待测数据的属性向量
                  vector.append(float(data[i]))
              elif classifier.format[i] == 'class':
                  classInColumn = i
        theClass= classifier.classify(vector) #返回预测分类的结果
        prefix = '-' #默认分类错误
        if theClass == data[classInColumn]: #判断分类是否正确
            # it is correct
            numCorrect += 1
            prefix = '+'
        print("%s  %12s  %s" % (prefix, theClass, line))
    print("%4.2f%% correct" % (numCorrect * 100/ len(lines)))

##
##  Here are examples of how the classifier is used on different data sets
##  in the book.
#  test('athletesTrainingSet.txt', 'athletesTestSet.txt')
#  test("irisTrainingSet.data", "irisTestSet.data")
#  test("mpgTrainingSet.txt", "mpgTestSet.txt")
