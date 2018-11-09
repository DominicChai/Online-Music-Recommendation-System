#歌曲是行
#用户是列
#推荐策略：找和你最相似的用户 推荐他听过但是你没有听过的歌曲
import numpy as np
import math

def Cosine(vec1, vec2):
    npvec1, npvec2 = np.array(vec1), np.array(vec2)
    return npvec1.dot(npvec2)/(math.sqrt((npvec1**2).sum()) * math.sqrt((npvec2**2).sum()))
music = ['Dreams', 'Rock and Roll', 'Blue'] #其实就不用指定music name li了 id就成

def recommendation(mat,target_uid):

    number_of_users=mat.shape[0]
    number_of_musics=mat.shape[1]

    target_row_index = target_uid - 1  # 真正对应用户的数据行
    print(mat[target_row_index, :])
    if set(mat[target_row_index, :])==set([0]):#冷启动
        return None,None

    max_row = (None, 0)
    none_null_index_list = []
    for i in range(number_of_musics):
        if mat[target_row_index, i] != 0:
            none_null_index_list.append(i)

    print('not null index is')
    print(none_null_index_list)

    for i in range(number_of_users):
        if i != target_row_index:  # 不和自己计算相似度
            # 计算相似度的时候 只计算两个用户都打过分的列：进一步的策略是：只取target user打过分的列
            similarity = Cosine(mat[target_row_index, none_null_index_list], mat[i, none_null_index_list])
            if similarity > max_row[1]:
                max_row = (i, similarity)

    print(max_row)

    # 取出target_user没有mark但是和他相似度最高的用户mark为4，5的歌曲set
    music_set = []
    for i in range(number_of_musics):
        if mat[max_row[0], i] >= 4 and mat[target_row_index, i] == 0:
            music_set.append(i+1) #note：range是从0开始的

    print(music_set)

    try:
        music_id=music_set.pop() #即使有多个音乐 只随机弹出一个音乐
    except:
        music_id=None

    similar_user_id=max_row[0]+1

    return music_id,similar_user_id

#print(Cosine([0,1],[1,2]))
#传进去的是两个list
#number_of_musics=len(music)
#number_of_users=5
#行数 列数

mat = np.zeros((5,3)) #基础打分都是0

#print(mat.shape)

mat[0,0] = 5
mat[0,1]=5
mat[0,2]=5

mat[3,0] = 1
mat[3,1]=1
mat[3,2]=1


mat[4,0]=5
mat[4,2]=4

print(mat)
#决定对哪一个用户推荐
#target_uid=5 #numpy的行下标和列下标是从0开始的


print(recommendation(mat,5))




