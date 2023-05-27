#!/usr/bin/env python
# coding: utf-8

# # 基于文本的推荐系统
# ## 学号：3220221155 姓名：桂梦婷
# 
# ### 1. 数据预处理
# 数据集来源为Yelp，由于文件过大，需要采取按行读取的方式。数据集选取方式如下，首先读取20000条交互数据，然后选取包含评价超过2条的商品，取其信息和对应用户(预期用户超过100个)

# In[1]:


import json
import random
import time

import pandas as pd
import numpy as np
from textblob import TextBlob
review_path = r"G:\code\data_mining\homework3\yelp_dataset\yelp_academic_dataset_review.json"
user_path = r"G:\code\data_mining\homework3\yelp_dataset\yelp_academic_dataset_user.json"


# In[2]:


user_dics = []
count = 0
with open(review_path, 'r', encoding="utf-8") as f:
    for line in f:
        if count > 20000:
            break
        temp_dic = json.loads(line)
        user_dics.append([temp_dic["review_id"],temp_dic["user_id"],temp_dic["business_id"],temp_dic["stars"],temp_dic["text"]])
        count += 1


# In[3]:


print(user_dics[0])


# In[4]:


df = pd.DataFrame(user_dics, columns=['review_id','user_id','business_id','stars','text'])
df['review_id'] = df['review_id'].astype(np.str)
df['user_id'] = df['user_id'].astype(np.str)
df['business_id'] = df['business_id'].astype(np.str)
df['stars'] = df['stars'].astype(np.int)
df['text'] = df['text'].astype(np.str)


# 可以看到已经保留了评论数不为1的数据，接下来随机选取100件商品，并在对他们的评论中挑选100条；再挑选100个用户信息中的id/useful/funny/cool三种评价的数值

# 统计商品的售卖次数，可以看到选取的2w条内存在对同一条商品的评价，于是随机选取100条评价次数不为1的商品。

# In[5]:


last = 0
count = 0
for i in df['business_id'].value_counts():
    if i == 1:
        last = count
        break
    count += 1


# In[6]:


print(df['business_id'].value_counts())


# In[102]:


good_ids = df['business_id'].value_counts().index.tolist()[10:last]
new_df = df[df["business_id"].isin(good_ids)]
print(new_df["business_id"].value_counts())


# 

# In[136]:


goods = random.sample(good_ids, 100)
final_df = df[df["business_id"].isin(goods)]
user_id_list = random.sample(final_df["user_id"].value_counts().index.tolist(),100)
final_df = final_df[final_df["user_id"].isin(user_id_list)]
final_df = final_df[final_df["business_id"].isin(goods)]
final_df = final_df.sample(n=100)
print(final_df)


# 选定了用户和商品后，接下来需要获取用户信息，并将收集的用户-商品购买信息处理成分析所需的格式。

# In[137]:


# 获取用户信息，并写入dataframe中
print(len(user_id_list))
user_df = pd.DataFrame(columns=['user','user_id','average_stars','useful','funny','cool'])
user_df['user'] = user_df['user'].astype(np.int32)
user_df['user_id'] = user_df['user_id'].astype(str)
user_df['average_stars'] = user_df['average_stars'].astype(np.float64)
user_df['useful'] = user_df['useful'].astype(np.int32)
user_df['funny'] = user_df['funny'].astype(np.int32)
user_df['cool'] = user_df['cool'].astype(np.int32)
user_info_list = []
user_count = 0
with open(user_path, 'r', encoding="utf-8") as f:
    for line in f:
        temp_dic = json.loads(line)
        if temp_dic["user_id"] in user_id_list and temp_dic["user_id"] not in user_df["user_id"]:
            # user user_id average_stars useful funny cool
            user_df = user_df.append({'user':user_count,'user_id':temp_dic["user_id"],'average_stars':temp_dic["average_stars"],'useful':temp_dic["useful"],'funny':temp_dic["funny"],'cool':temp_dic["cool"]},ignore_index=True)
            user_count += 1
        if user_count > 100:
            break
# user_df = pd.DataFrame(user_info_list, columns=['user','user_id','average_stars','useful','funny','cool'])


# 下面建立user_item_dict，即通过new_df中item和user的对应关系写入字典，此处user/item都已使用数字id代替

# In[138]:


print(user_df)


# In[139]:


print(len(list(set(user_df["user_id"]))))
print(len(list(set(final_df["user_id"]))))
# print(len(user_df[user_df["user_id"].isin(final_df["user_id"])]))
print(len(list(set(final_df["user_id"]) - set(user_df["user_id"]))))


# In[140]:


# user_平均评分，avg_stars
user_score_avg_list = list(user_df["average_stars"])
# user_item对应的词典
user_item_dict = {}
item_df = pd.DataFrame(columns=["item","item_id"])
item_df['item'] = item_df['item'].astype(np.int32)
item_df['item_id'] = item_df['item_id'].astype(str)
id_count = 0
for line in range(len(final_df)):
    uid = user_df[user_df["user_id"] == final_df.iloc[line]["user_id"]]["user"].values[0]
    iid = final_df.iloc[line]["business_id"]
    if uid not in user_item_dict:
        if item_df is not None and iid not in list(item_df["item_id"]):
            user_item_dict[uid] = [id_count]
            item_df = item_df.append({"item":id_count,"item_id":iid},ignore_index=True)
            id_count += 1
        else:
            user_item_dict[uid] = [item_df[item_df["item_id"]  == final_df.iloc[line]["business_id"]]["item"].values[0]]
    else:
        if item_df is not None and iid not in list(item_df["item_id"]):
            user_item_dict[uid].append([id_count])
            item_df = item_df.append({"item":id_count,"item_id":iid},ignore_index=True)
            id_count += 1
        else:
            user_item_dict[uid].append([item_df[item_df["item_id"]  == final_df.iloc[line]["business_id"]]["item"].values[0]])
print(item_df)


# 在步骤1中，获得了100件商品和100个用户，除了用户购买商品的100条记录（包含评论和评分）外，还有用户总评价数量（分别包含funny / cool / useful）。接下来将定义关联规则，为用户推荐商品。

# ### 2. 关联规则定义
# 根据常识定义以下规则:
# 1)用户的评论如果情感倾向为负面，则用户不喜欢该商品；反之，如果用户评论情感倾向为正面，则用户喜欢该商品。
# 2)如果用户评论情感倾向性并不是很明显，则观察其评分，如果评分有明显的倾向，则将其归类；若评分中庸，则倾向于用户不喜欢该商品。
# 3)如果用户评论的情感倾向和评分的倾向截然相反，即存在“高分低评”、“低分高评”的现象，则统一归为用户不推荐该商品。
# 4)用户总评价数量分布相似的用户，其偏好可能相似。
# 
# #### 2.1情感极性分析方法
# 情感极性分析方法采用textblob包，该工具可以用于英文文本情感分析，输入一个句子，输出其情感极性值。如果正面情感大于0.6，则认为用户喜欢该商品；如果负面情感小于-0.6，则认为用户不喜欢该商品；其余得分状况下，观察用户的评分倾向，在倾向相同的情况下，如果是1-3分，则认为用户不推荐该商品；如果是4-5分，则认为用户推荐该商品。若倾向不同，则认为用户不推荐该商品。

# In[185]:


user_item_arr = [[0 for i in range(0,100)] for i in range(0,100)]
# ['review_id','user_id','business_id','stars','text']
for line in range(len(item_df)):
    text = final_df.iloc[line]["text"]
    blob = TextBlob(text)
    #获取情感极性值
    sentiment = blob.sentiment.polarity
    right_pair = sentiment * (final_df.iloc[line]["stars"] - 2.5)
    # 如果对应正确，-1-1缩放到0-5
    final_score = (final_df.iloc[line]["stars"] + (sentiment+1)/2*5)/2
    # 获取用户和物品的id
    uid = user_df[user_df["user_id"] == final_df.iloc[line]["user_id"]]["user"].values[0]
    iid = item_df[item_df["item_id"] == final_df.iloc[line]["business_id"]]["item"].values[0]
    user_item_arr[uid][iid] = final_score
user_item_mat = user_item_arr


# #### 2.2 用户相似度矩阵构成
# 前面提到设置的关联规则中，具有相似评论分布的用户是相似的，实现方法为使用评论分布作为用户向量，按照向量的相似程度规定用户和用户的相似分数。
# 首先在user所属的DataFrame中，添加一列user_no，记录user_id和user_no的对应关系。
# 然后计算每个user的用户向量, 归一化后，根据该向量生成用户相似度矩阵

# In[220]:


import numpy as np
import time
# user user_id average_stars useful funny cool
user_no_df = user_df.copy()
user_vec_list = []
for line in range(len(user_no_df)):
    temp_vec = [user_no_df.iloc[line]["funny"], user_no_df.iloc[line]["cool"], user_no_df.iloc[line]["useful"]]
    all_vec = sum([i*i for i in temp_vec])
    if all_vec == 0:
        final_vec = [0,0,0]
    else:
        final_vec = [int(temp_vec[0])*1.0/all_vec,int(temp_vec[1])*1.0/all_vec,int(temp_vec[2])*1.0/all_vec]
    user_vec_list.append(final_vec)
user_vec_array = np.array(user_vec_list)
user_vec_matrix = np.mat(user_vec_array)
user_sim_matrix = 1 - user_vec_matrix * user_vec_matrix.T
user_sim_matrix = user_sim_matrix.tolist()
print(user_sim_matrix[0][0])


# ### 3. 用户 - 物品推荐
# 获取了用户相似度矩阵，和用户购买商品的矩阵后，采用基于用户的协同过滤方法为用户推荐商品。
# 对于每个用户，首先寻找相似用户（距离最近的用户）；其次，计算推荐值。
# 为此定义函数find_sim_users，输入为用户user_id，最大相似数目max_num, 输出为相似用户词典：该词典的key为相似用户id，value为词典，包含score（用户相似度分数），item（该用户购买的物品）
# 定义函数find_pred_items，输入为用户user_id, 用户相似用户和购买商品，输出为字典：key为物品id，value为推荐倾向得分。

# In[226]:


def find_sim_users(user_id, max_num):
    sim_users_dic = {}
    for i in range(len(user_sim_matrix[user_id])):
        if i == user_id:
            continue
        else:
            sim_users_dic[i] = user_sim_matrix[user_id][i]
    # 排序后的tuple
    s_tuple = sorted(sim_users_dic.items(), key=lambda x: x[1], reverse=True)
    count = 0
    sim_item_dic = {}
    for sim_user_id, sim_score in enumerate(s_tuple):
        # item去掉user_id对应用户购买过的商品
        sim_item_dic[sim_user_id] = {"score": sim_score,
                                     "items": list(set(user_item_dict[sim_user_id]) - set(user_item_dict[user_id]))}
        count += 1
        if count >= max_num:
            break
    return sim_item_dic


# In[231]:


def find_pred_items(user_id, sim_item_dic):
    item_pred_dic = {}
    # 遍历sim_item_dic，计算推荐度
    for users, user_info in sim_item_dic.items():
        for now_item in user_info["items"]:
            if now_item not in item_pred_dic:
                # 开始计算
                temp_score = 0
                temp_users = []
                for users2, user_info2 in sim_item_dic.items():
                    if now_item in user_info2["items"]:
                        temp_users.append(users2)
                sim_sum = sum([user_sim_matrix[user_id][i] for i in temp_users])
                sim_weight = sum(
                    [user_sim_matrix[user_id][i] * (user_item_mat[i][now_item] - user_score_avg_list[user_id]) for i in
                     temp_users])
                temp_score = user_score_avg_list[user_id] + sim_weight / sim_sum
                item_pred_dic[now_item] = temp_score
    return item_pred_dic


pred_item_dic = {}
for user in range(0, len(user_df)):
    sim_users = find_sim_users(user, 5)
    pred_items = find_pred_items(user, sim_users)
    pred_item_dic[user] = pred_items


# 计算完推荐度后，可以呈现预测结果。

# In[232]:


print(pred_item_dic)


# In[ ]:




