# 利用neo4j实现的豆瓣图书推荐系统
## 1.数据来源
* 用户评分数据来自于[北京大学开放数据研究平台](http://opendata.pku.edu.cn/)中的[豆瓣评分数据集](http://opendata.pku.edu.cn/dataset.xhtml?persistentId=doi:10.18170/DVN/LA9GRH)
* 图书数据爬取自豆瓣读书，根据评分数据集中的图书id进行匹配爬取
## 2.数据总量
* 图书数据 8W
* 用户评分数据 400w+

## 代码文件
* Spider - 爬虫相关
* data - 公开数据集
* neo4j - 数据库相关


