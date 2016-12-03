#
#
#  Nearest Neighbor Classifier for mpg dataset
#
#  for chapter 5 page 14
#
#  Code file for the book Programmer's Guide to Data Mining
#  http://guidetodatamining.com
#
#  Ron Zacharski
# crossValidation :交叉验证
import copy
class Classifier:
    #参数1:文件地址-包括文件头,使用时需要先使用divide.py进行数据10分割
    #参数2:文件num
    #参数3:列格式
    def __init__(self, bucketPrefix, testBucketNumber, dataFormat):
        """ a classifier will be built from files with the bucketPrefix
        excluding the file with textBucketNumber. dataFormat is a string that
        describes how to interpret each line of the data files. For example,
        for the mpg data the format is:
        "class	num	num	num	num	num	comment"
        """
        self.medianAndDeviation = [] #deviation:偏差
        # reading the data in from the file
        self.format = dataFormat.strip().split('\t') #获取格式到列表self.format
        self.data = [] #存放单条完整的格式化数据
        # for each of the buckets numbered 1 through 10:
        #对于01-10的每一个分割数据
        for i in range(1, 11): #i in 1-10
            # if it is not the bucket we should ignore, read in the data
            #此处巧妙,根据重新计算i对比上一个传过来的测试数据i,
            #比如传过来的测试数据时mpgData-01,testBucketNumber 为 1,
            #此处将针对02-10的数据进行读取,即使用02-10作为模型训练
            if i != testBucketNumber:
                #########################
                ### 读取文本
                filename = "%s-%02i" % (bucketPrefix, i)
                #print(filename)
                f = open(filename)
                lines = f.readlines()
                f.close()
                ###
                #########################
                for line in lines:
                    fields = line.strip().split('\t')
                    ignore = [] #存放注释,格式:[注释]
                    vector = [] #存放属性,格式:[属性1,属性2]
                    for j in range(len(fields)): #按照fields 列项目对比
                        if self.format[j] == 'num':
                            #vector.append(int(fields[j])) #<---此处使用int会报错,原因是该数据是一个字符串显示的浮点数
                            vector.append(round(float(fields[j])))
                        elif self.format[j] == 'comment':
                            ignore.append(fields[j])
                        elif self.format[j] == 'class':
                            classification = fields[j] #定义一个临时变量存放分类,字符串类型
                    self.data.append((classification, vector, ignore)) #格式为:('分类字符串', [属性1,属性2], 注释)
        #此处使用copy模块的deepcopy函数,采用深度复制
        self.rawData = copy.deepcopy(self.data)
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

    #参数1:文件地址-包括文件头,使用时需要先使用divide.py进行数据10分割
    #参数2:待测文件(测试数据)编号
    def testBucket(self, bucketPrefix, bucketNumber):
        """Evaluate the classifier with data from the file
        bucketPrefix-bucketNumber"""
        #########################
        ### 读取文本
        filename = "%s-%02i" % (bucketPrefix, bucketNumber)
        f = open(filename)
        lines = f.readlines()
        totals = {}
        f.close()
        ###
        #########################
        for line in lines:
            data = line.strip().split('\t')
            vector = []
            classInColumn = -1 #分类所在列的列号
            #按照格式列的个数读取列数据
            for i in range(len(self.format)):
                  if self.format[i] == 'num':
                      vector.append(float(data[i])) #按照格式读取data中的属性赋值给vector列表
                  elif self.format[i] == 'class':
                      classInColumn = i #获取分类信息所在列的列号
            theRealClass = data[classInColumn] #读取分类信息
            classifiedAs = self.classify(vector) #根据已知向量进行分类预测
            totals.setdefault(theRealClass, {}) #设置key1:totals为{'真实分类':{}}
            totals[theRealClass].setdefault(classifiedAs, 0) #嵌套的子字典为{'真实分类':{'预测分类1':0},{'预测分类2':0},...}
            totals[theRealClass][classifiedAs] += 1 #给对应的预测分类累加计数
        return totals

    ##################################################
    #### 计算曼哈顿距离
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
    ###
    ##################################################

#参数1:文件地址-包括文件头,使用时需要先使用divide.py进行数据10分割
#参数2:文件列格式
def tenfold(bucketPrefix, dataFormat):
    results = {}
    #i 取值 1~10:对应文件mpgData-01~mpgData-10
    for i in range(1, 11):
        c = Classifier(bucketPrefix, i, dataFormat)
        #交叉测试函数,训练归一化除i以外的文件数据后,
        #文件i的数据开始进行测试
        #返回单次文件的"混淆矩阵"
        t = c.testBucket(bucketPrefix, i)
        ##################################################
        ### 注意!!现在还在i的循环内,一共需要10次循环交叉验证
        ### 下面的results将每次交叉验证的t结果累加!!!
        for (key, value) in t.items(): #('真实分类', {'预测分类':数值})
            results.setdefault(key, {}) #设定格式{'真实分类', {'预测分类':数值}}
            for (ckey, cvalue) in value.items(): #获取嵌套字典的key和值
                results[key].setdefault(ckey, 0)
                results[key][ckey] += cvalue
        ###
        ##################################################
    # now print results
    categories = list(results.keys()) #获取'真实分类'的key
    categories.sort() #键值排序

    ##################################################
    ### 打印输出的格式,标题栏,表格框
    print(   "\n       Classified as: ")
    header =    "        "
    subheader = "      +"
    for category in categories:
        header += category + "   "
        subheader += "----+"
    print (header)
    print (subheader)
    ###
    ##################################################
    ### 计算正确率,输出混淆矩阵
    total = 0.0
    correct = 0.0
    for category in categories:
        row = category + "    |"
        for c2 in categories:
            if c2 in results[category]:
                count = results[category][c2]
            else:
                count = 0
            row += " %2i |" % count
            total += count
            if c2 == category:
                correct += count
        print(row)
    print(subheader)
    print("\n%5.3f percent correct" %((correct * 100) / total))
    print("total of %i instances" % total)

if __name__ == "__main__":
    tenfold("mpgData/mpgData",        "class	num	num	num	num	num	comment")
