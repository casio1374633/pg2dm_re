#
#  FILTERINGDATA.py
#
#  Code file for the book Programmer's Guide to Data Mining
#  http://guidetodatamining.com
#  Ron Zacharski
#
#  代码注释:casio 2016-11-21
#
from math import sqrt

#字典联合,这种方式很棒
users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }


# 计算曼哈顿距离
def manhattan(rating1, rating2):
    """Computes the Manhattan distance. Both rating1 and rating2 are dictionaries
       of the form {'The Strokes': 3.0, 'Slightly Stoopid': 2.5}"""
    distance = 0
    commonRatings = False 
    total = 0 #此处添加自文件filteringdataPearson.py
    for key in rating1:
        if key in rating2:
            distance += abs(rating1[key] - rating2[key])
            commonRatings = True
            total += 1 #计算有多少个相同属性项 c_ad:filteringdataPearson.py
        #------------ c_ad -------------
        # 此处使用了自己的认知: 原代码没有
        # 如果出现缺失值,即一个用户对某产品评价而另一用户没有评价,则使用最大评价值
        else:
             distance += 5
             commonRatings = True
             total += 1 #计算有多少个相同属性项 c_ad:filteringdataPearson.py
        #------------ c_ad -------------
    #如果产生了距离值(即至少有一个属性有共同评价)
    if commonRatings:
        return distance / total #计算平均值,这种做法更合理
    else:
        return -1 #Indicates no ratings in common 没有相同评价则返回-1(即最大值)

# 计算最近邻
#username是指的待测用户,users指用户集合
def computeNearestNeighbor(username, users):
    """creates a sorted list of users based on their distance to username"""
    distances = [] #距离记录使用列表方式
    for user in users: #循环查找每个用户
        if user != username: #自己和自己不做判断
            distance = manhattan(users[user], users[username])
            distances.append((distance, user)) #记录距离['距离','用户名']
    # sort based on distance -- closest first
    distances.sort() #距离排序,最小的放前面
    # print(distances)
    return distances

#username是指的待测用户,users指用户集合
def recommend(username, users):
    """Give list of recommendations"""
    # first find nearest neighbor
    #获取距离最近的用户名称,仅针对名称,不获取得分
    nearest = computeNearestNeighbor(username, users)[0][1]
    print(nearest)
    recommendations = []
    # now find bands neighbor rated that user didn't
    #最近邻用户的全部信息
    neighborRatings = users[nearest]
    print(neighborRatings)
    #带测用户的全部信息
    userRatings = users[username]
    print(userRatings)
    #------------ c_note -------------
    #遍历最近邻用户的每一个评分项
    for artist in neighborRatings: 
        if not artist in userRatings: #如果不在待测用户的字典里则添加到推荐当中
            recommendations.append((artist, neighborRatings[artist]))
    # using the fn sorted for variety - sort is more efficient
    #
    #此句的sorted使用了倒序排列,评分最高的放前面
    #lambda里面的内容是,已列名是artistTuple,以第二列为排序重点
    #reverse = True 表示倒序
    return sorted(recommendations, key=lambda artistTuple: artistTuple[1], reverse = True)
    #------------ c_note -------------
"""
>>> student_tuples = [
        ('john', 'A', 15),
        ('jane', 'B', 12),
        ('dave', 'B', 10),
]
>>> sorted(student_tuples, key=lambda student: student[2])   # sort by age
[('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
"""
# examples - uncomment to run

print( recommend('Hailey', users))
#print( recommend('Chan', users))
