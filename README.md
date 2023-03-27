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

### 作业3说明

alzheimer首先对每列属性进行可视化，分析其逻辑关系和缺失情况，从而采取诸如删除列、采用中位数补充缺失值等方法对缺失值进行处理，具体内容请于ipynb文件中查看。

movieLen数据集包含3个表格，通过查看和分析，仅对rating.dat进行缺失值填充，具体内容请于对应ipynb文件中查看。
