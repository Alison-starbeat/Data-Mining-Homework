#!/usr/bin/env python
# coding: utf-8

# ### 1 数据分析
# #### 1.1 数据分析目的
# 该数据集的主题是一系列关于疾病的调查，其中地理位置、受调查人的个人情况也囊括在内，我认为其最终目的为在给定环境和人员基本情况下，预测他们的患病概率，以对他们的健康生活做出指导。首先需要先观察数据。
# #### 1.2 数据摘要
# 该数据集为csv格式，可以非常方便利用csv相关的函数对表头进行读取，以获取数据集包含的信息。

# In[5]:


import csv
import matplotlib.pyplot as plt
import pandas as pd
# dataPath = "G:\\gmt\\data_mining\\homework2\\dataset"
dataPath = "C:\\Users\\gui\\Desktop\\homework2\\dataset"


# In[6]:


with open(dataPath+"\\alzheimer\\Alzheimer Disease and Healthy Aging Data In US.csv","r",encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    print(header)
    print("属性列共有{}".format(len(header)))
    df = pd.read_csv(dataPath+"\\alzheimer\\Alzheimer Disease and Healthy Aging Data In US.csv",header = 0)


# 可以看到数据集包含非常多列，观察它们，我们可以粗略地对相关的数据列进行分类：
# 1. 数据收集时间(2)：YearStart,YearEnd
# 2. 数据收集位置(4)：LocationAbbr,LocationDesc(前两项分别是地理位置的简写和称);Geolocation;LocationID(它们都代表了具体的位置和对应id)
# 3. 疾病类型(6)：Class,ClassID;Topic,TopicID;Question,QuestionID(研究的健康问题、主题、具体研究问题)
# 4. 疾病评估数值(7)：Data_Value_Unit,DataValueTypeID,Data_Value_Type(有关数据的形式);Data_Value,Data_Value_Alt(有关数值);Low_Confidence_Limit,High_Confidence_Limit(数据的置信度)
# 5. 研究对象属性(8)：StratificationCategoryID1,StratificationCategory1,StratificationID1,Stratification1(属性1和对应值);
#                StratificationCategoryID2,StratificationCategory2,StratificationID2,Stratification2(属性2和对应值)
# 6. 数据来源(1):DataSource
# 7. 其他(1)：Sample_Size
# 接下来分别对各类数据的基本情况进行分析。

# In[7]:


na_columns = df.loc[:, (df.isnull().any())].columns


# ##### 1.2.1 数据收集时间、收集位置、数据来源
# 首先对数据收集时间、收集位置、数据来源各自的数据分布进行一定的可视化分析。
# （1） 数据收集时间

# In[8]:


df["YearStart"] = df["YearStart"].values.astype(int)
print(df["YearStart"].describe())


# In[9]:


df["YearEnd"] = df["YearEnd"].values.astype(int)
print(df["YearEnd"].describe())


# In[10]:


# TODO：这里需要先统计数量，然后再写成词典，然后再绘图
year = {}
for i in range(0,len(df["YearStart"])):
    if df["YearStart"][i] in year:
        if df["YearEnd"][i] in year[df["YearStart"][i]]:
            year[df["YearStart"][i]][df["YearEnd"][i]] += 1
        else:
            year[df["YearStart"][i]][df["YearEnd"][i]] = 1
    else:
        year[df["YearStart"][i]] = {}
        if df["YearEnd"][i] in year[df["YearStart"][i]]:
            year[df["YearStart"][i]][df["YearEnd"][i]] += 1
        else:
            year[df["YearStart"][i]][df["YearEnd"][i]] = 1
print(year)


# In[11]:


year_order = [(k,year[k]) for k in sorted(year.keys())]
# print(year_order)


# In[12]:


width = 0.15
posMove = 0
color = {2015:"red",2016:"blue",2017:"green",2018:"yellow",2019:"purple",2020:"grey"}
x = []
y = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
for key,item in year_order:
    x.append(key)
    for endYear,num in item.items():
        y[endYear-2015][key-2015] = num
# print(y)
plt.figure(figsize=(10,6))
for data in range(0,len(y)):
    realYear = data+2015
    plt.bar([i+posMove*width for i in x],y[data],width=0.15,color=color[data+2015],label=str(realYear))
    posMove += 1
    for a,b in zip(x,y[data]):
        plt.text(a+posMove*width-0.15, b, '%.0f' % b, ha='center', va= 'bottom',fontsize=11)

plt.legend()
plt.show()


# 以开始时间开始为横坐标，探究调查持续时间可以发现，除2015年以外，其余疾病调查均为1年内数据；而2015年开始的调查中，有10960条持续了5年（至2020年终止）。且可以发现，这两列数据并无缺失值和错误值（即开始时间大于结束时间）。
# 
# （2）数据收集位置
# 首先分析该数据是否存在缺失值和错误值，该数据可能出现的错误值情况为ID、位置简写和位置全称不对应的情况。

# In[13]:


# 数据值是否有缺失,总数据条数为214462条
# LocationAbbr,LocationDesc;Geolocation;LocationID
missLocAbbr = 0
for dat in df["LocationAbbr"]:
    if dat == "":
        missLocAbbr += 1
print(missLocAbbr)

missLocDesc = 0
for dat in df["LocationDesc"]:
    if dat == "":
        missLocDesc += 1
print(missLocDesc)

missLocGeo = 0
for dat in df["Geolocation"]:
    if dat == "":
        missLocGeo += 1
print(missLocGeo)

missLocID = 0
for dat in df["LocationID"]:
    if dat == "":
        missLocID += 1
print(missLocID)


# 观察结果，发现地理位置无缺失值，然后统计调查位置分布和ID与位置的对应关系，分析数据是否存在错误值，以下代码运行后，可以发现全称和简写、具体地理位置坐标和ID均为一一对应，无错误;接下来判断具体地理坐标ID是否与地区一一对应，均为一一对应。

# In[14]:


locDic = {}
locGeoDic = {}
locIDDescDic = {}
# 记录错误数据行数
# locDic = {"位置全称":"简写"}
wrongData = []
for line in range(0,214462):
    locDesc = df["LocationDesc"][line]
    locAbbr = df["LocationAbbr"][line]
    locID = df["LocationID"][line]
    locGeo = df["Geolocation"][line]

    if locDesc in locDic:
        if locAbbr != locDic[locDesc]:
            wrongData.append(line)
    else:
        locDic[locDesc] = locAbbr

    if locID in locGeoDic:
        if locGeo not in locGeoDic[locID]:
            locGeoDic[locID].append(locGeo)
            wrongData.append(line)
    else:
        locGeoDic[locID] = [locGeo]

    if locID in locIDDescDic:
        if locDesc not in locIDDescDic[locID]:
            locIDDescDic[locID].append(locDesc)
            wrongData.append(line)
    else:
        locIDDescDic[locID] = [locDesc]


print("错误对应的数量为：{}".format(len(wrongData)))
# print(locGeoDic)


# 判断完是否有缺失值后，对调查案例的地区分布进行简单的分析。可以发现大部分区域均选取约3000人进行跟进调查，而Virgin Island跟踪调查人物较少。

# In[15]:


dicLoc = {}
for line in range(0, 214462):
    locDesc = df["LocationDesc"][line].strip("\n")
    if locDesc in dicLoc:
        dicLoc[locDesc] += 1
    else:
        dicLoc[locDesc] = 1
dicLoc_order = {}
for j in sorted(dicLoc.keys()):
    dicLoc_order[j] = dicLoc[j]
# print(dicLoc_order)
plt.figure(figsize=(10,16))
plt.xlabel("location")

plt.xticks(fontsize=12)
plt.ylabel("numbers")
x = list(dicLoc_order.keys())
y = list(dicLoc_order.values())
# print(x)
for a, b in zip(x,y):
     plt.text(b+4,a, '%.0f' % b, horizontalalignment='center', fontsize=9)
plt.barh(x,y,height=0.8)
plt.show()


# （3） 疾病类型(6)：Class,ClassID;Topic,TopicID;Question,QuestionID(研究的健康问题、主题、具体研究问题)
# 疾病类型的处理逻辑和地理位置的处理逻辑一致，不过多赘述，结果发现仍无错误对应关系

# In[16]:


disClassDic = {}
disTopicDic = {}
disQuesDic = {}
# 记录错误数据行数
wrongData = []
for line in range(0,214462):
    disClass = df["Class"][line]
    disClassID = df["ClassID"][line]
    disTopic = df["Topic"][line]
    disTopicID = df["TopicID"][line]
    disQues = df["Question"][line]
    disQuesID = df["QuestionID"][line]

    if disClassID in disClassDic:
        if disClass not in disClassDic[disClassID]:
            disClassDic[disClassID].append(disClass)
            wrongData.append(line)
    else:
        disClassDic[disClassID] = [disClass]

    if disTopicID in disTopicDic:
        if disTopic not in disTopicDic[disTopicID]:
            disTopicDic[disTopicID].append(disTopic)
            wrongData.append(line)
    else:
        disTopicDic[disTopicID] = [disTopic]

    if disQuesID in disQuesDic:
        if disQues not in disQuesDic[disQuesID]:
            disQuesDic[disQuesID].append(disQues)
            wrongData.append(line)
    else:
        disQuesDic[disQuesID] = [disQues]


print("错误对应的数量为：{}".format(len(wrongData)))


# 接下来将对研究课题数量进行一定的分析。取研究大类作为横坐标，分析研究大类中不同主题的数量；以及以不同主题为横坐标，研究不同主题研究的不同问题的方向。发现问题与主题一一对应，而不同大类中存在着许多的主题，其分布大致平均。

# In[17]:


dicClassTopic = {}
dicTopicQues = {}
for line in range(0,214462):
    disClass = df["Class"][line]
    disTopic = df["Topic"][line]
    disQuesID = df["QuestionID"][line]
    if disClass in dicClassTopic:
        if disTopic in dicClassTopic[disClass]:
            dicClassTopic[disClass][disTopic] += 1
        else:
            dicClassTopic[disClass][disTopic] = 1
    else:
        dicClassTopic[disClass] = {}
        dicClassTopic[disClass][disTopic] = 1

    if disTopic in dicTopicQues:
        if disQuesID in dicTopicQues[disTopic]:
            dicTopicQues[disTopic][disQuesID] += 1
        else:
            dicTopicQues[disTopic][disQuesID] = 1
    else:
        dicTopicQues[disTopic] = {}
        dicTopicQues[disTopic][disQuesID] = 1


# In[18]:


width = 0.15
for key in dicClassTopic.keys():
    plt.figure(figsize=(13,6))
    # plt.xticks(rotation=-20)
    plt.xlabel("Topics of {}".format(key))
    plt.ylabel("Numbers")
    for a,b in zip(dicClassTopic[key].keys(),dicClassTopic[key].values()):
        plt.text(b+230, a,'%.0f' % b, ha='center',fontsize=11)
    plt.barh(list(dicClassTopic[key].keys()), dicClassTopic[key].values(),color='b',height=0.8)
    plt.show()


# In[19]:


width = 0.15
plt.figure(figsize=(13,6))
# plt.xticks(rotation=-20)
plt.xlabel("Topics of Overall Health")
plt.ylabel("Numbers")
for a,b in zip(dicClassTopic["Overall Health"].keys(),dicClassTopic["Overall Health"].values()):
    plt.text(b+230, a,'%.0f' % b, ha='center',fontsize=11)
plt.barh(list(dicClassTopic["Overall Health"].keys()), dicClassTopic["Overall Health"].values(),color='b')


# （4）疾病评估数值(7)：
# Data_Value_Unit,DataValueTypeID,Data_Value_Type(有关数据的形式)
# 疾病评估形式等处理逻辑如上所示，同样发现无缺失和错误对应值。
# Data_Value,Data_Value_Alt(有关数值);Low_Confidence_Limit,High_Confidence_Limit(数据的置信度)
# 而观察原始数据，发现有关数字的数值有明显缺失，统计分析其缺失属性所属课题和地区，以为接下来的数据缺失处理打下基础。

# In[20]:


dfDataValue = pd.DataFrame([df["Data_Value"],df["Data_Value_Alt"],df["Low_Confidence_Limit"],df["High_Confidence_Limit"]])


# In[21]:


missDataValue = []
for line in range(0,len(df["Data_Value"])):
    if not pd.notnull(dfDataValue[line]["Data_Value"]):
        missDataValue.append(line)
# print(missDataValue)
print("缺失属性值个数为:{}，占全部数据的{}".format(len(missDataValue),len(missDataValue)/214462))


# 发现属性缺失值约有32%，此处需要建立模型拟合，从而填补空缺值。
# 对于离群点的处理，需要先绘制盒图，并采用五点法观察其特征,此处分析参见2.3小节。

# （5）研究对象属性
# StratificationCategoryID1,StratificationCategory1,StratificationID1,Stratification1(属性1和对应值)
# StratificationCategoryID2,StratificationCategory2,StratificationID2,Stratification2(属性2和对应值)
# 首先初步观察数据可以得知，属性1和属性2均为调查对象属性，即使有缺失值也无法采用模型预测（调查对象并不符合一定的原则标准，性别和种族无法通过患病率预测），因此对于单列缺失值的处理方式为简单填充Unknown，若存在数据2个属性均缺失，需要综合该数据其他缺失值进行进一步评估和处理。

# In[22]:


dicStr = {}
missStratification = [[],[]]
# dicStr = {“cateID":{"name":,"attr":{"ID":值}}}
for line in range(0,214462):
    strCate1 = df["StratificationCategory1"][line]
    strCateID1 = df["StratificationCategoryID1"][line]
    str1 = df["Stratification1"][line]
    strID1 = df["StratificationID1"][line]
    strCate2 = df["StratificationCategory2"][line]
    strCateID2 = df["StratificationCategoryID2"][line]
    str2 = df["Stratification2"][line]
    strID2 = df["StratificationID2"][line]

    if pd.notnull(strCate1):
        if strCateID1 in dicStr:
            if strID1 not in dicStr[strCateID1]["attr"]:
                dicStr[strCateID1]["attr"][strID1] = str1
            elif str1 != dicStr[strCateID1]["attr"][strID1]:
                missStratification.append(line)
        else:
            dicStr[strCateID1] = {}
            dicStr[strCateID1]["name"] = strCate1
            dicStr[strCateID1]["attr"] = {}
            dicStr[strCateID1]["attr"][strID1] = str1
    else:
        missStratification[0].append(line)

    if pd.notnull(strCate2):
        if strCateID2 in dicStr:
            if strID2 not in dicStr[strCateID2]["attr"]:
                dicStr[strCateID2]["attr"][strID2] = str2
            elif str2 != dicStr[strCateID2]["attr"][strID2]:
                missStratification.append(line)
        else:
            dicStr[strCateID2] = {}
            dicStr[strCateID2]["name"] = strCate2
            dicStr[strCateID2]["attr"] = {}
            dicStr[strCateID2]["attr"][strID2] = str2
    else:
        missStratification[1].append(line)


# 可以发现属性2有27669条缺失值，约占全部数据条数的13%左右，对于这些缺失值暂时不做处理。

# （6）数据来源和其他
# 仅剩的DataSource和Sample_Size放到一起进行分析

# In[24]:


missData = [[],[]]
dicOther = {"Datasource":[],"Sample_Size":[]}
for line in range(0,214462):
    if pd.notnull(df["Datasource"][line]):
        if df["Datasource"][line] not in dicOther["Datasource"]:
            dicOther["Datasource"].append(df["Datasource"][line])
    else:
        missData[0].append(line)

    if pd.notnull(df["Sample_Size"][line]) and df["Sample_Size"][line] not in dicOther["Sample_Size"]:
         dicOther["Sample_Size"].append(df["Sample_Size"][line])
    else:
        missData[1].append(line)


# In[25]:


print(dicOther)
print(len(missData[0]))
print(len(missData[1]))


# 可以发现Datasource来源单一，且Sample_Size列为数据完全缺失的列，因此删除Sample_Size列。
# 
# #### 1.3 数据总结
# 在1.2对数据情况进行分析后，可以发现部分数据存在缺失：
# ① 患病率和置信区间：缺失约32%左右，需建立模型进行拟合，填补缺失值
# ② 调查对象属性2：缺失约13%左右，无法采取有效方式填补缺失值（由于性别和种族无法被有效预测），使用Unknown填补所有缺失值
# ③ 数据样本尺寸：缺失值为100%，删除该列
# 
# ### 2 数据缺失处理办法
# #### 2.1 Sample_Size
# 该数据列100%缺失，予以去除，其具体方法为去除DataFrame中的Sample_Size列，可以看到已经成功地删除了Sample_Size列

# In[26]:


dfCopy = df.copy()


# In[27]:


try:
    dfCopy = dfCopy.drop('Sample_Size',axis='columns')
except KeyError as error:
    print(error)
print(dfCopy.head(0))


# #### 2.2 Stratification2,StratificationID2
# 简单采取StratificationCategory2填充Attrib,Stratification2填充Unknown方式填补缺失值

# In[28]:


dfCopy['StratificationCategory2'].fillna("Attrib", inplace=True)
dfCopy['Stratification2'].fillna("Unknown", inplace=True)


# #### 2.3 Data_Value,Data_Value_Alt(有关数值);Low_Confidence_Limit,High_Confidence_Limit(数据的置信度)
# 这些数据列缺失值较多，需要先观察缺失数据的属性。研究对象有年份、地区、年龄、第二属性（性别或种族或未知），需要先进行研究问题的筛选后，探究这些属性对研究问题的影响。首先要计算属性相关性，根据相关情况进行填充。

# In[29]:


# missDataValue列表中存放着缺失数据值的行编号
dicLossID = {}
for line in missDataValue:
    if dfCopy["QuestionID"][line] not in dicLossID:
        dicLossID[df["QuestionID"][line]] = [line]
    else:
        dicLossID[df["QuestionID"][line]].append(line)


# In[30]:


print(dicLossID.keys())


# 对于不同问题而言，如果存在离群点，则将其全部处理为箱线图上限。

# In[31]:


for key in dicLossID.keys():
    quesID = key
    tempDf = df[(df.QuestionID == key)]
    # 获取了所有数据行之后，从中取出有数据值的数据，分别分析它们与年份、地区、年龄、第二属性的关系
    tempDfNotNull = tempDf[tempDf["Data_Value"].notna()]
    plt.boxplot(tempDfNotNull["Data_Value"])
    plt.grid(linestyle="--", alpha=0.3)
    plt.show()
    print(tempDfNotNull["Data_Value"].describe())

    iqr = tempDfNotNull["Data_Value"].describe()["75%"] - tempDfNotNull["Data_Value"].describe()["25%"]
    upLine = iqr*1.5 + tempDfNotNull["Data_Value"].describe()["75%"]
    downLine =  tempDfNotNull["Data_Value"].describe()["25%"] - iqr*1.5


# In[32]:


dfCopy['Low_Confidence_Limit'] = pd.to_numeric(dfCopy['Low_Confidence_Limit'], errors='coerce')
dfCopy['High_Confidence_Limit'] = pd.to_numeric(dfCopy['High_Confidence_Limit'], errors='coerce')
corr_matrix = dfCopy.corr()


# In[33]:


for column in na_columns[:4]:
    highest_corr = corr_matrix[column].sort_values(ascending=False).index[1]
    dfCopy[column].fillna(dfCopy[highest_corr].mean(), inplace=True)


# 对于剩余的属性（dataValue,dataValueAlt,low/highConfidence），可以找到最相似的行进行填充

# In[39]:


for column in na_columns[:4]:
    dfCopy[column].fillna(dfCopy[column].mean(), inplace=True)

for column in na_columns[5:]:
    dfCopy[column].fillna(dfCopy[column].mode().iloc[0], inplace=True)


# In[40]:


dfCopy.to_csv(dataPath+"\\alzheimer\\new Alzheimer.csv")


# ### 3 数据集处理前后对比
# 首先查看数据属性个数，可以看到处理后数据列数减少。

# In[41]:


with open(dataPath+"\\alzheimer\\Alzheimer Disease and Healthy Aging Data In US.csv","r",encoding="utf-8") as f:
    oldReader = csv.reader(f)
    oldReader = next(oldReader)
    oldDf = pd.read_csv(dataPath+"\\alzheimer\\Alzheimer Disease and Healthy Aging Data In US.csv",header = 0)
    print("原数据集共有{}列属性，分别是：".format(len(oldReader)))
    print(oldReader)

with open(dataPath+"\\alzheimer\\new Alzheimer.csv","r",encoding="utf-8") as f:
    newReader = csv.reader(f)
    newReader = next(newReader)
    newDf = pd.read_csv(dataPath+"\\alzheimer\\new Alzheimer.csv",header = 0)
    print("共有{}列属性，分别是：".format(len(newReader)))
    print(newReader)


# In[42]:


print("旧数据集缺失率：")
print((oldDf.isnull().sum())/oldDf.shape[0])


# In[43]:


print("新数据集缺失率：")
print((newDf.isnull().sum())/newDf.shape[0])

