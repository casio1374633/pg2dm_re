#
#  Naive Bayes Classifier chapter 6
#
# _____________________________________________________________________
import math
class Classifier:
    def __init__(self, bucketPrefix, testBucketNumber, dataFormat):
        """ a classifier will be built from files with the bucketPrefix
        excluding the file with textBucketNumber. dataFormat is a string that
        describes how to interpret each line of the data files. For example,
        for the iHealth data the format is:
        "attr	attr	attr	attr	class"
        """
        total = 0 #统计示例总数
        classes = {}
        # counts used for attributes that are not numeric
        counts = {}
        # totals used for attributes that are numereric
        # we will use these to compute the mean and sample standard deviation for
        # each attribute - class pair.
        totals = {}
        numericValues = {}
        # reading the data in from the file
        self.format = dataFormat.strip().split('\t') #获取格式到列表self.format
        #
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
                    nums = []
                    for i in range(len(fields)): #按照fields 列项目对比
                        if self.format[i] == 'num':
                            nums.append(float(fields[i]))
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
                    totals.setdefault(category, {})
                    numericValues.setdefault(category, {})
                    classes[category] += 1
                    ###
                    #####################################
                    # now process each non-numeric(非数值型) attribute of the instance
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
                    # process numeric attributes (计算数值型属性)
                    col = 0
                    for columnValue in nums:
                        col += 1
                        totals[category].setdefault(col, 0)
                        #totals[category][col].setdefault(columnValue, 0)
                        totals[category][col] += columnValue
                        numericValues[category].setdefault(col, [])
                        numericValues[category][col].append(columnValue)
        #
        # ok done counting. now compute probabilities
        #
        # first prior probabilities p(h)
        # 计算先验概率
        for (category, count) in classes.items():
            self.prior[category] = count / total #先验概率为分类项个数 / 总数
        #
        # now compute conditional probabilities p(h|D)
        # 计算条件概率
        for (category, columns) in counts.items():
              self.conditional.setdefault(category, {})
              for (col, valueCounts) in columns.items():
                  self.conditional[category].setdefault(col, {})
                  for (attrValue, count) in valueCounts.items(): #attrValue:属性, count:计数
                      self.conditional[category][col][attrValue] = (
                          count / classes[category])
        self.tmp =  counts
        #
        # now compute mean and sample standard deviation
        # 计算均值
        self.means = {}

#        self.totals = totals
        for (category, columns) in totals.items():
            self.means.setdefault(category, {})
            for (col, cTotal) in columns.items():
                self.means[category][col] = cTotal / classes[category]
        # standard deviation 计算标准差
        self.ssd = {}
        for (category, columns) in numericValues.items():
            self.ssd.setdefault(category, {})
            for (col, values) in columns.items():
                SumOfSquareDifferences = 0
                theMean = self.means[category][col]
                for value in values:
                    SumOfSquareDifferences += (value - theMean)**2
                columns[col] = 0
                self.ssd[category][col] = math.sqrt(SumOfSquareDifferences / (classes[category]  - 1))
 # test the code
c = Classifier("pimaSmall/pimaSmall",  1, "num	num	num	num	num	num	num	num	class")
# test means computation
assert(c.means['1'][1] == 5.25)
assert(round(c.means['1'][2], 4) == 146.0556)
assert(round(c.means['0'][2], 4) == 111.9057)
# test standard deviation
assert(round(c.ssd['0'][1], 4) == 2.5469)
assert(round(c.ssd['1'][8], 4) == 10.9218)
print("Means and SSD computation appears OK")