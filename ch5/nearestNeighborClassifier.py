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
    #alist���б�,һ����
    def getMedian(self, alist):
        """return median of alist"""
        if alist == []:
            return []
        #���б�����
        blist = sorted(alist)
        length = len(alist)
        #�ж���ż
        if length % 2 == 1:
            #���������,�򷵻��м�ֵ
            # length of list is odd so return middle element
            return blist[int(((length + 1) / 2) -  1)]
        else:
            #�����ż��,�����м�����ֵ��ƽ��ֵ
            # length of list is even so compute midpoint
            v1 = blist[int(length / 2)]
            v2 =blist[(int(length / 2) - 1)]
            return (v1 + v2) / 2.0

    #������Ա�׼��
    def getAbsoluteStandardDeviation(self, alist, median):
        """given alist and median return absolute standard deviation"""
        sum = 0
        for item in alist:
            sum += abs(item - median) #sum(x_i - ��λ��)
        return sum / len(alist) #sum / ���� = ���Ա�׼��

    #��һ������,����������к�
    def normalizeColumn(self, columnNumber):
        """given a column number, normalize that column in self.data"""
        # first extract values to list
        #col���б�,��ŵ���ȫ��self.data������i����ֵ
        col = [v[1][columnNumber] for v in self.data] #vΪself.data���ж�ȡ,v[1][columnNumber]��ȡ�����б��еĵ�i����ֵ
        #��ȡ��λ��ֵ(�����е��м�ֵ)
        median = self.getMedian(col)
        #����asd,����P109ҳ�й�ʽ"���Ա�׼��"
        asd = self.getAbsoluteStandardDeviation(col, median)
        #print("Median: %f   ASD = %f" % (median, asd))
        #medianAndDeviation�����λ���;��Ա�׼��,��ʽΪԪ��:(��λ��,���Ա�׼��)
        #����medianAndDeviationΪ�б�,ÿ����Ԫ��Ԫ��.[(��λ��1,���Ա�׼��1), (��λ��2, ���Ա�׼��2)]
        self.medianAndDeviation.append((median, asd))
        #��������i��ÿ����ֵ�ĸĽ���׼����
        for v in self.data:
            #��ʽ��P109ҳ,"(ÿ��ֵ - ��λ��) / ���Ա�׼�� = �Ľ��ı�׼����"
            v[1][columnNumber] = (v[1][columnNumber] - median) / asd

    #�Դ����û������Թ�һ��
    def normalizeVector(self, v):
        """We have stored the median and asd for each column.
        We now use them to normalize vector v"""
        #list(v)��v��һ�µ�,v��������б�
        vector = list(v)
        for i in range(len(vector)):
            #��ȡ��Ӧ���Ե�(��λ��,���Ա�׼��)
            (median, asd) = self.medianAndDeviation[i]
            #��һ����Ӧ���Ե���ֵ
            vector[i] = (vector[i] - median) / asd
        return vector
    ###
    ### END NORMALIZATION
    ##################################################

    #���������پ���
    def manhattan(self, vector1, vector2):
        """Computes the Manhattan distance."""
        return sum(map(lambda v1, v2: abs(v1 - v2), vector1, vector2))


    #def nearestNeighbor(self, itemVector):
    #    """return nearest neighbor to itemVector"""
    #    return ((0, ("REPLACE THIS LINE WITH CORRECT RETURN", [0], [])))
    #����Ϊ�����û��������б�
    def nearestNeighbor(self, itemVector):
        """return nearest neighbor to itemVector"""
        #�Ը����Լ���ÿ���û������������پ���,�������Сֵ
        #��ʽΪ:[(�û�1�������б�,(����,[�����б�],ע��)), (�û�2�������б�,(����,[�����б�],ע��))]
        return min([ (self.manhattan(itemVector, item[1]), item) #�˴�itemΪdata��һ��,item[1]��ȡ�����б�
                     for item in self.data])
    #��������������С�ڽ��ķ�����
    def classify(self, itemVector):
        """Return class we think item Vector is in"""
        return(self.nearestNeighbor(self.normalizeVector(itemVector))[1][0]) #��������ĸ�ʽ,��֪��ȡitem�еķ����ַ���
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

#��py�ʺ���python������ʹ��import����,�������ע��������д��ʽ
#���������Զ����ͬ�����ݼ�
def test(training_filename, test_filename):
    """Test the classifier on a test set of data"""
    #��һ��ѵ�����ݼ�
    classifier = Classifier(training_filename)
    ##################################################
    ### �򿪲������ݼ�
    f = open(test_filename)
    lines = f.readlines()
    f.close()
    ###
    ##################################################

    ##################################################
    #������ȷ��
    numCorrect = 0.0 #��ȷ����
    for line in lines:
        data = line.strip().split('\t')
        vector = []
        classInColumn = -1
        for i in range(len(classifier.format)):
              if classifier.format[i] == 'num': #��ȡ�������ݵ���������
                  vector.append(float(data[i]))
              elif classifier.format[i] == 'class':
                  classInColumn = i
        theClass= classifier.classify(vector) #����Ԥ�����Ľ��
        prefix = '-' #Ĭ�Ϸ������
        if theClass == data[classInColumn]: #�жϷ����Ƿ���ȷ
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
