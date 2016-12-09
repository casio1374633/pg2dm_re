#NewsGroup语料库,P244页
import os, codecs, math
class BayesText:
    def __init__(self, trainingdir, stopwordlist):
        """This class implements a naive Bayes approach to text
        classification
        trainingdir is the training data. Each subdirectory of
        trainingdir is titled with the name of the classification
        category -- those subdirectories in turn contain the text
        files for that category.
        The stopwordlist is a list of words (one per line) will be
        removed before any counting takes place.
        """
        #词汇字典,格式:{'词汇1':出现次数, '词汇2':出现次数,...}
        self.vocabulary = {}
		#self.prob格式:
        #{'分类1':{'词汇1':统计次数1, '词汇2':次数2,...},
        # '分类2':{'词汇1':统计次数1, '词汇2':次数2,...},...}
        #----------------------------------------------------
        #之后的格式:
        #{'分类1':{'词汇1':出现概率1, '词汇2':出现概率2,...},
        # '分类2':{'词汇1':出现概率1, '词汇2':出现概率2,...},...}
        self.prob = {}  
        self.totals = {} #格式:{'分类1':共处理N1个词汇, '分类2':共处理N2个词汇,...}
        self.stopwords = {} #格式:{'停词1':1, '停词2':1, ...}
        ###############################
        ### 输入停词
        ### self.stopwords = {'停词1':1, '停词2':1, ...}
        f = open(stopwordlist)
        for line in f:
            self.stopwords[line.strip()] = 1
        f.close()
        ###
        ###############################
        categories = os.listdir(trainingdir) #列表形式:列出所有trainingdir下的1级文件夹
        #filter out files that are not directories
        self.categories = [filename for filename in categories
                           if os.path.isdir(trainingdir + filename)]
        print("Counting ...")
        ###############################
        ### 对每一个分类进行训练
        for category in self.categories:
            print('    ' + category)
            #category是分类名,trainingdir对应训练根目录 I am going to eliminate any word in the vocabulary
            #self.prob放入分类词汇字典.
            #格式:
            #{'分类1':{'词汇1':统计次数1, '词汇2':次数2,...},
            # '分类2':{'词汇1':统计次数1, '词汇2':次数2,...},...}
            #-----------------------------------------------------
            #self.totals存放每个分类下一共处理了多少个词汇
            (self.prob[category], self.totals[category]) = self.train(trainingdir, category)
        ########################################
        # 在总体词汇字典中,出现次数小于3次的,都统计到toDelete列表内,后面好删除
        # that doesn't occur at least 3 times
        toDelete = []
        for word in self.vocabulary:
            if self.vocabulary[word] < 3:
                # mark word for deletion
                # can't delete now because you can't delete
                # from a list you are currently iterating over
                toDelete.append(word)
        # now delete
        #对应待删除的列表,逐项查找self.vocabulary,如果有就把该项删除.减轻词汇字典
        for word in toDelete:
            del self.vocabulary[word]
        ########################################
        # now compute probabilities
        vocabLength = len(self.vocabulary) #计算词汇字典的词汇量
        print("Computing probabilities:") #计算贝叶斯概率
        ########################################
        ### 采用书上P232页的算法计算概率
        for category in self.categories:
            print('    ' + category)
            denominator = self.totals[category] + vocabLength
            for word in self.vocabulary:
                if word in self.prob[category]:
                    count = self.prob[category][word]
                else:
                    count = 1
                #self.prob的形式发生了变化:
                #之前的格式:
                #{'分类1':{'词汇1':统计次数1, '词汇2':次数2,...},
                # '分类2':{'词汇1':统计次数1, '词汇2':次数2,...},...}
                #----------------------------------------------------
                #之后的格式:
                #{'分类1':{'词汇1':出现概率1, '词汇2':出现概率2,...},
                # '分类2':{'词汇1':出现概率1, '词汇2':出现概率2,...},...}
                self.prob[category][word] = (count + 1) / denominator
        print ("DONE TRAINING\n\n") #完成分类概率统计
        ###
        ########################################
    ########################################
    #数据训练函数
    #参数1:训练文件夹
    #参数2:训练分类
    def train(self, trainingdir, category):
        """counts word occurrences for a particular category"""
        currentdir = trainingdir + category #训练文件夹的绝对地址
        files = os.listdir(currentdir) #列出所有待训练的文件名
        counts = {} #词汇字典计数,和self.vocabulary内容一致
        total = 0 #统计词汇字典一共处理了多少个词汇
        #依次读取待训练文件
        for file in files:
            #print(currentdir + '/' + file)
            f = codecs.open(currentdir + '/' + file, 'r', 'iso8859-1') #获取文件句柄,并设置读取编码
            #按行读取文件
            for line in f:
                #获取文本数据分隔数据,列表形式
                tokens = line.split()
                for token in tokens:
                    # get rid of punctuation and lowercase token
                    #读取列表内的词组
                    token = token.strip('\'".,?:-') #删除不必要的字符
                    token = token.lower() #全部小写
                    if token != '' and not token in self.stopwords: #如果字符串不为空并且不在停词列表内
                        #self.vocabulary 和counts内容在单次循环内一致,可以这么认为
                        #self.voca是所有训练文件的汇总性词库字典,
                        #counts是单次分类的词库字典
                        self.vocabulary.setdefault(token, 0) #设置词汇字典格式
                        self.vocabulary[token] += 1
                        counts.setdefault(token, 0)
                        counts[token] += 1
                        total += 1
            f.close()
        return(counts, total) #返回单次分类的词汇字典和该文件一共处理了多少个有效词汇
    ########################################
    ### 测试分类函数
    ### 参数1:待测分类文件地址
    def classify(self, filename):
        results = {}
        for category in self.categories:
            results[category] = 0
        f = codecs.open(filename, 'r', 'iso8859-1')
        for line in f:
            tokens = line.split()
            for token in tokens:
                #print(token)
                token = token.strip('\'".,?:-').lower()
                if token in self.vocabulary:
                    for category in self.categories:
                        if self.prob[category][token] == 0:
                            print("%s %s" % (category, token))
                        #获取对应文字在每个分类下的贝叶斯概率值
                        results[category] += math.log(self.prob[category][token])
        f.close()
        results = list(results.items()) #将字典变成列表嵌套元祖的方式,格式:[('分类1',概率值),('分类2',概率值),...]
        results.sort(key=lambda tuple: tuple[1], reverse = True)
        # for debugging I can change this to give me the entire list
        return results[0][0] #倒序排序后输出最大值,即贝叶斯概率最大的预测分类
########################################
### 主程序
if __name__ == "__main__":
    # change these to match your directory structure
    trainingDir = ".\\20news-bydate\\20news-bydate-train\\"
    # (just create an empty file to use as a stoplist file.)
    stoplistfile = "stopwords25.txt"
    bT = BayesText(trainingDir, stoplistfile)
    print("Running Test ...")
    result = bT.classify(".\\20news-bydate\\20news-bydate-test\\rec.motorcycles\\104673")
    print(result)
    result = bT.classify(".\\20news-bydate\\20news-bydate-test\\sci.med\\59246")
    print(result)
    result = bT.classify(".\\20news-bydate\\20news-bydate-test\\soc.religion.christian\\21424")
    print(result)
###
########################################
