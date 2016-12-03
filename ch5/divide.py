#P148页,分层采样方法将数据分到10个桶中
# divide data into 10 buckets
#引入随机数
import random

_debug = 1

#参数:输入文件名,输出分割文件的文件名,分割符,分类信息在哪一类
def buckets(filename, bucketName, separator, classColumn):
    """the original data is in the file named filename
    bucketName is the prefix(翻译:字首) for all the bucket names
    separator is the character that divides the columns
    (for ex., a tab or comma and classColumn is the column
    that indicates the class"""

    # put the data in 10 buckets
    numberOfBuckets = 10 #分割10份
    data = {} #读取输入文件的数据,字典模式
    ###############################################
    # first read in the data and divide by category
    #整行读取
    with open(filename) as f:
        lines = f.readlines()
    ###
    ###############################################
    debug_i = 0
    for line in lines:
        #此处我认为写的不好,强行转换成'\t'形式反而容易出错
        #if separator != '\t':
        #    line = line.replace(separator, '\t')
        ## first get the category
        #category = line.split()[classColumn]
        #-------- c_add ------------
        category = line.split(separator)[classColumn] #<---字符串分割列表后读取分类信息
        #-------- c_add ------------
        #设定字典关键字为分类,默认值为空列表[] {分类1:['行1信息','行2信息','行3信息',...], 分类2:['行1信息','行2信息','行3信息',...]}
        data.setdefault(category, [])
        data[category].append(line)
        if _debug:
            if debug_i == 100:
                print(data)
                print("="*20)
                debug_i += 1
            else:
                debug_i += 1
    # initialize the buckets

    ###############################################
    ### 对分割数据初始化
    buckets = [] #列表模式
    debug_i = 0
    for i in range(numberOfBuckets):
        buckets.append([]) #增加嵌套列表 [[],[],...]
    # now for each category put the data into the buckets
    for k in data.keys(): #获取data键值 k取值为:'10','20','30' <--为分类的种类数
        #randomize order of instances for each class
        random.shuffle(data[k]) #此处巧妙,分类后面跟着的是一个列表,random.shuffle负责把列表的数据随机化
        bNum = 0
        # divide into buckets
        ###############################################
        #此处很有技巧,看了调试才发现
        #首先上面一个for循环保证在data[k]内都是同一个类别,然后依次从该列表里,每次取出一个数据(即一行信息)
        #依次放入0,1,2,3,4,5,6,7,8,9,0,1,2,3,4...如此循环
        #这样就能保证每个数据都是均匀放入
        #print("-"*30)
        for item in data[k]: #获取分类中的列表数据
            buckets[bNum].append(item)
            bNum = (bNum + 1) % numberOfBuckets #加1取余,保证0~9

    #通过下面这行print可以印证
    #print(buckets[0])
    ###
    ###############################################

    # write to file
    for bNum in range(numberOfBuckets):
        f = open("%s-%02i" % (bucketName, bNum + 1), 'w')
        for item in buckets[bNum]: #依次写入[0~9]
            f.write(item)
        f.close()

# example of how to use this code
#buckets("pimaSmall.txt", 'pimaSmall',',',8)
buckets("mpgData.txt", 'mpgData','\t',0)
