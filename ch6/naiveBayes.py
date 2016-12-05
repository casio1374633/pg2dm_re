#
#  Naive Bayes Classifier chapter 6
#
# _____________________________________________________________________
#iHealth属性列的中文意思
#-------------------------------------
#main interest:主要的兴趣|current exercise level:当前运动水平|how motivated:动机|comfortable with tech devices:使用设备是否习惯|which model:使用的哪种型号
#both,health,appearance:外观|sedentary:久坐,active:活跃,moderate:适度温和|moderate:适度温和,aggressive:剧烈|yes,no|i100,i500
class Classifier:
    def __init__(self, bucketPrefix, testBucketNumber, dataFormat):
        """ a classifier will be built from files with the bucketPrefix
        excluding the file with textBucketNumber. dataFormat is a string that
        describes how to interpret each line of the data files. For example,
        for the iHealth data the format is:
        "attr	attr	attr	attr	class"
        """
        total = 0 #统计示例总数
        classes = {} #
        counts = {}
        # reading the data in from the file
        self.format = dataFormat.strip().split('\t') #获取格式到列表self.format
        self.prior = {} #先验概率哈希表 {'分类1':概率1, '分类2':概率2,...}
        #条件概率,格式为:
        #{'分类1':{列1:{'列1中变量1':条件概率,'列1中变量2':条件概率,...},
        #          列2:{'列2中变量1':条件概率,'列2中变量2':条件概率,...},
        #          列3:{...}},
        # '分类2':{列1:{'列1中变量1':条件概率,'列1中变量2':条件概率,...},
        #          列2:{'列2中变量1':条件概率,'列2中变量2':条件概率,...},
        #          列3:{...}}}
        self.conditional = {}
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
                    for i in range(len(fields)): #按照fields 列项目对比
                        if self.format[i] == 'num':
                            vector.append(float(fields[i]))
                        elif self.format[i] == 'attr':
                            vector.append(fields[i])
                        elif self.format[i] == 'comment':
                            ignore.append(fields[i])
                        elif self.format[i] == 'class':
                            category = fields[i]
                    #####################################
                    # now process this instance
                    ### 此部分计算先验概率
                    #{'democrat': 111, 'republican': 97}
                    total += 1
                    classes.setdefault(category, 0) #分类计数格式:{'分类1':计数1, '分类2':计数2,...}
                    counts.setdefault(category, {})
                    classes[category] += 1
                    ###
                    #####################################
                    # now process each attribute of the instance
                    ### 此部分计算条件概率
                    # {'分类1': {列1:{'属性1':计数1,'属性2':计数2}, 列2:{'属性1':计数1,'属性2':计数2}
                    #           列2:{'属性1':计数1,'属性2':计数2}, 列2:{'属性1':计数1,'属性2':计数2}},
                    #  '分类2': {列1:{'属性1':计数1,'属性2':计数2}, 列2:{'属性1':计数1,'属性2':计数2}
                    #           列2:{'属性1':计数1,'属性2':计数2}, 列2:{'属性1':计数1,'属性2':计数2}}
                    # }
                    #{'democrat': {1: {'n': 50, 'y': 61}, 2: {'n': 61, 'y': 50}, 3: {'n': 17, 'y': 94},
                    #              4: {'n': 105, 'y': 6}, 5: {'n': 86, 'y': 25}, 6: {'n': 60, 'y': 51},
                    #              7: {'n': 27, 'y': 84}, 8: {'n': 20, 'y': 91}, 9: {'n': 25, 'y': 86},
                    #              10: {'n': 52, 'y': 59}, 11: {'n': 53, 'y': 58}, 12: {'n': 95, 'y': 16},
                    #              13: {'n': 77, 'y': 34}, 14: {'n': 71, 'y': 40}, 15: {'n': 47, 'y': 64},
                    #              16: {'n': 6, 'y': 105}},
                    # 'republican': {1: {'n': 79, 'y': 18}, 2: {'n': 54, 'y': 43}, 3: {'n': 82, 'y': 15},
                    #                4: {'n': 1, 'y': 96}, 5: {'n': 5, 'y': 92}, 6: {'n': 12, 'y': 85},
                    #                7: {'n': 72, 'y': 25}, 8: {'n': 82, 'y': 15}, 9: {'n': 85, 'y': 12},
                    #                10: {'n': 40, 'y': 57}, 11: {'n': 82, 'y': 15}, 12: {'n': 13, 'y': 84},
                    #                13: {'n': 17, 'y': 80}, 14: {'n': 2, 'y': 95}, 15: {'n': 85, 'y': 12},
                    #                16: {'n': 32, 'y': 65}}}
                    col = 0
                    for columnValue in vector:
                        col += 1
                        counts[category].setdefault(col, {})
                        counts[category][col].setdefault(columnValue, 0)
                        counts[category][col][columnValue] += 1
                    ###
                    #####################################
        #
        # ok done counting. now compute probabilities
        #
        # first prior probabilities p(h)
        # 计算先验概率
        for (category, count) in classes.items():
            self.prior[category] = count / total #先验概率为分类项个数 / 总数
        #
        # now compute conditional probabilities p(D|h)
        # 计算条件概率
        for (category, columns) in counts.items():
              self.conditional.setdefault(category, {})
              for (col, valueCounts) in columns.items():
                  self.conditional[category].setdefault(col, {})
                  for (attrValue, count) in valueCounts.items(): #attrValue:属性, count:计数
                      self.conditional[category][col][attrValue] = (
                          count / classes[category])
        self.tmp =  counts
    ###
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
        loc = 1
        for line in lines:
            loc += 1
            data = line.strip().split('\t')
            vector = []
            classInColumn = -1 #分类所在列的列号
            #按照格式列的个数读取列数据
            for i in range(len(self.format)):
                  if self.format[i] == 'num':
                      vector.append(float(data[i])) #按照格式读取data中的属性赋值给vector列表
                  elif self.format[i] == 'attr':
                      vector.append(data[i])
                  elif self.format[i] == 'class':
                      classInColumn = i #获取分类信息所在列的列号
            theRealClass = data[classInColumn] #读取分类信息
            #print("REAL ", theRealClass)
            classifiedAs = self.classify(vector) #根据已知向量进行分类预测
            totals.setdefault(theRealClass, {}) #设置key1:totals为{'真实分类':{}}
            totals[theRealClass].setdefault(classifiedAs, 0) #嵌套的子字典为{'真实分类':{'预测分类1':0},{'预测分类2':0},...}
            totals[theRealClass][classifiedAs] += 1 #给对应的预测分类累加计数
        return totals
    #预测分类
    def classify(self, itemVector):
        """Return class we think item Vector is in"""
        results = []
        for (category, prior) in self.prior.items():
            prob = prior
            col = 1
            for attrValue in itemVector:
                if not attrValue in self.conditional[category][col]: #如果待测示例对应列的选项不在训练库内,则概率是0
                    # we did not find any instances of this attribute value
                    # occurring with this category so prob = 0
                    prob = 0
                else: #如果在训练库内有对应的选项,则计算贝叶斯概率
                    prob = prob * self.conditional[category][col][attrValue]
                col += 1
            results.append((prob, category))
        # return the category with the highest probability
        return(max(results)[1]) #计算所有分类的贝叶斯概率,然后返回最大值
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
    print(   "\n            Classified as: ")
    header =    "             "
    subheader = "               +"
    for category in categories:
        header += "% 10s   " % category
        subheader += "-------+"
    print (header)
    print (subheader)
    ###
    ##################################################
    ### 计算正确率,输出混淆矩阵
    total = 0.0
    correct = 0.0
    for category in categories:
        row = " %10s    |" % category
        for c2 in categories:
            if c2 in results[category]:
                count = results[category][c2]
            else:
                count = 0
            row += " %5i |" % count
            total += count
            if c2 == category:
                correct += count
        print(row)
    print(subheader)
    print("\n%5.3f percent correct" %((correct * 100) / total))
    print("total of %i instances" % total)

if __name__ == "__main__":
    tenfold("house-votes/hv", "class\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr")
    print("--"*20)
    tenfold("mpgData/mpgData", "class	attr	num	num	num	num	comment")
    print("--"*20)
    c = Classifier("iHealth/i", 10,
                           "attr\tattr\tattr\tattr\tclass")
    print("choice: " + c.classify(['health', 'moderate', 'moderate', 'yes']))
#c = Classifier("house-votes/hv", 0,
#                       "class\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr")
#c = Classifier("iHealth/i", 10,
#                       "attr\tattr\tattr\tattr\tclass")
#print(c.classify(['health', 'moderate', 'moderate', 'yes']))
#c = Classifier("house-votes-filtered/hv", 5, "class\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr")
#t = c.testBucket("house-votes-filtered/hv", 5)
#print(t)
