import codecs 
from math import sqrt

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0,
                      "Norah Jones": 4.5, "Phoenix": 5.0,
                      "Slightly Stoopid": 1.5,
                      "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5,
                 "Deadmau5": 4.0, "Phoenix": 2.0,
                 "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0,
                  "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5,
                  "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0,
                 "Deadmau5": 4.5, "Phoenix": 3.0,
                 "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                 "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0,
                    "Norah Jones": 4.0, "The Strokes": 4.0,
                    "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0,
                     "Norah Jones": 5.0, "Phoenix": 5.0,
                     "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                     "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0,
                 "Norah Jones": 3.0, "Phoenix": 5.0,
                 "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0,
                      "Phoenix": 4.0, "Slightly Stoopid": 2.5,
                      "The Strokes": 3.0}
        }

class recommender:
    #user数据集, knn雏形 k个邻近, 算法使用毕尔逊算法, 最大推荐数为5
    def __init__(self, data, k=1, metric='pearson', n=5):
        """ initialize recommender
        currently, if data is dictionary the recommender is initialized
        to it.
        For all other data types of data, no initialization occurs
        k is the k value for k nearest neighbor
        metric is which distance formula to use
        n is the maximum number of recommendations to make"""
        self.k = k
        self.n = n
        self.username2id = {} #{地址:用户id}
        self.userid2name = {} #{用户id:地址+年龄(如果有年龄的话)}
        self.productid2name = {} #{isbn:书名+作者}
        # for some reason I want to save the name of the metric
        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson
        #
        # if data is dictionary set recommender data to it
        # 对输入的data类型进行检查,只有字典模式才能认可
        if type(data).__name__ == 'dict':
            self.data = data

    def convertProductID2name(self, id):
        """Given product id number return product name"""
        if id in self.productid2name:#productid2name->{isbn:书名+作者}
            return self.productid2name[id]
        else:
            return id

    def userRatings(self, id, n):
        """Return n top ratings for user with id"""
        print ("Ratings for " + self.userid2name[id])#{用户id:地址+年龄(如果有年龄的话)}

        ratings = self.data[id]
        #获取字典内book_isbn的个数
        print(len(ratings))
        #将字典转换成列表,好排序
        #将字典里面的book_isbn换成"书名+作者", 在通过元祖(k,v)把rate结合起来组成[(书名+作者,评分)]
        ratings = list(ratings.items())
        ratings = [(self.convertProductID2name(k), v)
                   for (k, v) in ratings]
        # finally sort and return
        ratings.sort(key=lambda artistTuple: artistTuple[1],
                     reverse = True)
        #指获取前5个
        ratings = ratings[:n]
        for rating in ratings:
            print("%s\t%i" % (rating[0], rating[1]))

    def loadBookDB(self, path=''):
        """loads the BX book dataset. Path is where the BX files are
        located"""
        self.data = {}
        i = 0
        #
        # First load book ratings into self.data
        # BX-Book-Ratings.csv "User-ID";"ISBN";"Book-Rating"
        newpath = path + "BX-Book-Ratings.csv"
        print(newpath)
        #------------ c_ad -------------
        #codes.open的用法
        #http://f.dataguru.cn/thread-237116-1-1.html
        #最近老被编码困扰，多次折腾之后，感觉python的编解码做得挺好的，只要了解下边的流程，一般都能解决
        #
        #input文件(gbk, utf-8...)   ----decode----->   unicode  -------encode------> output文件(gbk, utf-8...)
        #很多文本挖掘的package是在unicode上边做事的，比如nltk. 所以开始读入文件后要decode为unicode格式，可以通过下边两步：
        #f=open('XXXXX', 'r')
        #content=f.read().decode('utf-8')
        #
        #更好的方法是使用codecs.open读入时直接解码：
        #f=codecs.open(XXX, encoding='utf-8')
        #content=f.read()
        #------------ c_ad -------------
        f = codecs.open(newpath, 'r', 'utf8')
        for line in f: #逐行读取
            i += 1
            #separate line into fields
            #print(line)
            fields = line.split(';')
            user = fields[0].strip('"') #用户ID
            book = fields[1].strip('"') #ISBN号
            rating = int(fields[2].strip().strip('"')) #评分
            #--------- c_add ----------
            #采用的是字典嵌套字典的方式 {user-id:{book_isbn1:rate1, book_isbn2:rate2}}
            if user in self.data: #如果user这个key在之前的{}字典里能找到
                currentRatings = self.data[user] #获取该user对应的嵌套字典
            else:
                currentRatings = {} #如果没有,则创建字典(内层嵌套的字典,仅包含book_isbn:rate)
            currentRatings[book_isbn] = rating #添加内层字典{book_isbn:rate}
            self.data[user] = currentRatings #添加外层字典{user:{book_isbn:rate}}
        f.close()
        #
        # Now load books into self.productid2name
        # Books contains isbn, title, and author among other fields
        #"BX-Books.csv" :
        #"ISBN";"Book-Title";"Book-Author";"Year-Of-Publication";"Publisher";"Image-URL-S";"Image-URL-M";"Image-URL-L"
        f = codecs.open(path + "BX-Books.csv", 'r', 'utf8')
        for line in f:
            i += 1
            #separate line into fields
            fields = line.split(';')
            isbn = fields[0].strip('"') #添加isbn
            title = fields[1].strip('"') #添加书名
            author = fields[2].strip().strip('"') #添加作者
            title = title + ' by ' + author
            self.productid2name[isbn] = title #字典模式{isbn:书名+作者}
        f.close()
        #
        #  Now load user info into both self.userid2name and
        #  self.username2id
        #"BX-Users.csv":"User-ID";"Location";"Age"
        f = codecs.open(path + "BX-Users.csv", 'r', 'utf8')
        for line in f:
            i += 1
            #print(line)
            #separate line into fields
            fields = line.split(';')
            userid = fields[0].strip('"') #添加用户id
            location = fields[1].strip('"') #添加地址
            #============================================
            # if len(fields) > 3:
            #     age = fields[2].strip().strip('"')
            # else:
            #     age = 'NULL'
            # if age != 'NULL':
            #     value = location + '  (age: ' + age + ')'
            # else:
            #     value = location
            #判断年龄是否为空
            if len(fields) > 2:
                age = fields[2].strip().strip('"')
            else:
                age = 'NULL'
            if age != 'NULL':
                value = location + '  (age: ' + age + ')'
            else:
                value = location
            # ============================================
            self.userid2name[userid] = value #{用户id:地址+年龄(如果有年龄的话)}
            self.username2id[location] = userid #{地址:用户id}
        f.close()
        print(i) #显示读取了多少行的数据

    #计算皮尔逊距离
    def pearson(self, rating1, rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0
        # now compute denominator
        denominator = (sqrt(sum_x2 - pow(sum_x, 2) / n)
                       * sqrt(sum_y2 - pow(sum_y, 2) / n))
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator

    def computeNearestNeighbor(self, username):
        """creates a sorted list of users based on their distance to
        username"""
        distances = []
        #---------------------------------------
        #计算id:171118和data内所有id的皮尔逊距离
        for instance in self.data:
            if instance != username:
                distance = self.fn(self.data[username],
                                   self.data[instance])
                distances.append((instance, distance)) #添加到距离列表里(用户id, 距离)
        # sort based on distance -- closest first
        #按距离倒序排列,皮尔逊距离-1到1,所以1最近,一致性最好,不同于曼哈顿距离
        distances.sort(key=lambda artistTuple: artistTuple[1],
                       reverse=True)
        return distances
        #---------------------------------------

    def recommend(self, user):
        """Give list of recommendations"""
        recommendations = {}
        # first get list of users  ordered by nearness
        #获取最近距离人群的列表,包括(用户id,距离)
        nearest = self.computeNearestNeighbor(user)
        #
        # now get the ratings for the user
        #
        userRatings = self.data[user] #获取该用户的所有书籍评分{book_isbn:rate}
        #
        # determine the total distance
        totalDistance = 0.0
        for i in range(self.k): #self.k为knn个数,此处取1,即最近的1个
           totalDistance += nearest[i][1]
        # now iterate through the k nearest neighbors
        # accumulating their ratings
        for i in range(self.k):
           # compute slice of pie
           #应该是标准归一化,!!权重!!
           weight = nearest[i][1] / totalDistance
           # get the name of the person
           #获取最近用户的id
           name = nearest[i][0]
           # get the ratings for this person
           #获取该用户的所有书籍评分
           neighborRatings = self.data[name]
           # get the name of the person
           # now find bands neighbor rated that user didn't
           for artist in neighborRatings: #在最近邻用户里的所有book_isbn
              if not artist in userRatings: #如果不在被测用户的book_isbn里
                 if artist not in recommendations: #如果也不在推荐列表里
                    recommendations[artist] = (neighborRatings[artist] #添加字典{book_isbn:当前用户的权重评分}
                                               * weight)
                 else: #如果在列表里(指针对k>1的情况)
                    recommendations[artist] = (recommendations[artist] #之前的评分加上新的用户权重评分
                                               + neighborRatings[artist]
                                               * weight)
        # now make list from dictionary
        #将字典转换成列表,方便下面进行排序,recommendations字典内容包括{book_isbn:rate}
        recommendations = list(recommendations.items())
        #将字典里面的book_isbn换成"书名+作者", 在通过元祖(k,v)把rate结合起来组成[(书名+作者,评分)]
        recommendations = [(self.convertProductID2name(k), v)
                           for (k, v) in recommendations]
        # finally sort and return
        #按照第二列评分倒序输出
        recommendations.sort(key=lambda artistTuple: artistTuple[1],
                             reverse = True)
        # Return the first n items
        return recommendations[:self.n] #如果列表的个数比n小,则全部输出,此处不会出错

if __name__ == "__main__":
    r = recommender(users)
    # print(r.recommend('Jordyn'))
    # print(r.pearson(users['Angelica'], users['Bill']))
    r.loadBookDB('.\\')
    # BX-Book-Ratings.csv "User-ID";"ISBN";"Book-Rating"
    #------- c_ad -------
    shownum = 10 #显示前10行
    #print self.data
    print(70 * "=")
    cnt = 0
    for key in r.data.keys():
        if cnt < shownum:
            print("%s => %s" % (key, r.data[key])) #{user:{book_isbn:rate}}
            cnt += 1
        else:
            break
    #print self.productid2name
    print(70 * "=")
    cnt = 0
    for key in r.productid2name.keys():
        if cnt < shownum:
            print("%s => %s" % (key, r.productid2name[key])) #{isbn:书名+作者}

            cnt += 1
        else:
            break
    # print self.userid2name
    print(70 * "=")
    cnt = 0
    for key in r.userid2name.keys():
        if cnt < shownum:
            print("%s => %s" % (key, r.userid2name[key])) #{用户id:地址+年龄(如果有年龄的话)}

            cnt += 1
        else:
            break
    # print self.username2id
    print(70 * "=")
    cnt = 0
    for key in r.username2id.keys():
        if cnt < shownum:
            print("%s => %s" % (key, r.username2id[key])) #{地址:用户id}
            cnt += 1
        else:
            break
    #------- c_ad -------
    print(70 * ">")
    print(r.recommend('171118')) #计算用户ID:171118的推荐
    print(70*"=")
    print(r.userRatings('171118', 5)) #计算knn种k=5的情况
