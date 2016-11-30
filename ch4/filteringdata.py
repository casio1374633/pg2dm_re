#
#  ch4-filteringdata.py
#
#  Code for the first example from chapter 4.
#  The only change from the original filteringdata.py is the addition of the music dictionary.
#
#  Code file for the book Programmer's Guide to Data Mining
#  http://guidetodatamining.com
#  Ron Zacharski
#  2016-11-27(整个代码只是个引子,函数都是ch2的内容,直接参照即可,无需再做注释)

from math import sqrt

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }

music = {"Dr Dog/Fate": {"piano": 2.5, "vocals": 4, "beat": 3.5, "blues": 3, "guitar": 5, "backup vocals": 4, "rap": 1},
         "Phoenix/Lisztomania": {"piano": 2, "vocals": 5, "beat": 5, "blues": 3, "guitar": 2, "backup vocals": 1, "rap": 1},
         "Heartless Bastards/Out at Sea": {"piano": 1, "vocals": 5, "beat": 4, "blues": 2, "guitar": 4, "backup vocals": 1, "rap": 1},
         "Todd Snider/Don't Tempt Me": {"piano": 4, "vocals": 5, "beat": 4, "blues": 4, "guitar": 1, "backup vocals": 5, "rap": 1},
         "The Black Keys/Magic Potion": {"piano": 1, "vocals": 4, "beat": 5, "blues": 3.5, "guitar": 5, "backup vocals": 1, "rap": 1},
         "Glee Cast/Jessie's Girl": {"piano": 1, "vocals": 5, "beat": 3.5, "blues": 3, "guitar":4, "backup vocals": 5, "rap": 1},
         "La Roux/Bulletproof": {"piano": 5, "vocals": 5, "beat": 4, "blues": 2, "guitar": 1, "backup vocals": 1, "rap": 1},
         "Mike Posner": {"piano": 2.5, "vocals": 4, "beat": 4, "blues": 1, "guitar": 1, "backup vocals": 1, "rap": 1},
         "Black Eyed Peas/Rock That Body": {"piano": 2, "vocals": 5, "beat": 5, "blues": 1, "guitar": 2, "backup vocals": 2, "rap": 4},
         "Lady Gaga/Alejandro": {"piano": 1, "vocals": 5, "beat": 3, "blues": 2, "guitar": 1, "backup vocals": 2, "rap": 1}}

#这个方式过时,对于缺失数据有很大的问题
#参见ch2/filteringdata.py
def manhattan(rating1, rating2):
    """Computes the Manhattan distance. Both rating1 and rating2 are dictionaries
       of the form {'The Strokes': 3.0, 'Slightly Stoopid': 2.5}"""
    distance = 0
    total = 0
    for key in rating1:
        if key in rating2:
            distance += abs(rating1[key] - rating2[key])
            total += 1
    return distance

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

