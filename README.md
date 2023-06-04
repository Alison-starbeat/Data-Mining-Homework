# Data-Mining-Homework

A collection of homework

本仓库为BIT数据挖掘课程的作业存放仓库，学号3220221155。

### 文件构成

    -- homework3
    --- alzheimer_new.py
    --- alzheimer_new.ipynb
    本python文件对alzheimer数据集进行处理，并且生成处理后的数据集alzheimer_new.csv
    --- movielen.py
    --- movielen.ipynb
    本python文件对movieLen100M进行处理。
    --- dataset
    数据集，并未在本仓库实现
    ---- alzheimer
    ---- movieLen
    
    -- homework4
    --- hw4.py
    采用数据集为yelp，经过预处理得到了100个物品、100个用户（包含具体信息），以及100条交互记录文本
    --- hw4.ipynb
    
    -- homework5
    --- 报告.ipynb
    包含数据预处理、数据分析
    --- pdf
    报告pdf版本
    --- cnews
    数据集应该存放的部分，内应含stopwords.txt\cnews.test.txt，需要自行下载

### 作业3说明

alzheimer首先对每列属性进行可视化，分析其逻辑关系和缺失情况，从而采取诸如删除列、采用中位数补充缺失值等方法对缺失值进行处理，具体内容请于ipynb文件中查看。

movieLen数据集包含3个表格，通过查看和分析，仅对rating.dat进行缺失值填充，具体内容请于对应ipynb文件中查看。

### 作业4说明

首先处理Yelp数据集，仅保留user：user_id,avg_stars,cool,funny,useful，item:item_id（bussiness_id），以及review: user_id, bussiness_id, stars, text
然后进行关联规则规定和挖掘

### 作业5说明

挖掘对象：cnews数据集（新闻数据集），地址：https://blog.csdn.net/qq_36047533/article/details/88360833

选题背景：新闻无处不在，不同用户对新闻的偏好也是不同的，因此对新闻分类是极其有必要的。分类后的新闻可以按照类别进行呈现，方便观看。

本实验采用了test文件-cnews的文本部分，分类标签仅作为评测指标使用。
