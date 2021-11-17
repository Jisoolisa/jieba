import collections
import jieba
import os
import mysql.connector
cnn=mysql.connector.connect(host='localhost',port=3306,user='root',passwd='123690sweet.',database='Tian',charset='utf8')
cursor=cnn.cursor()
files=open(r"C:/Users/admin/Desktop/spider_news2.txt","r",encoding="utf-8").read()
path = os.getcwd()
jieba.load_userdict(os.path.join("C:/Users/admin/Desktop/dict.txt"))#导入自定义词典
seg_list_exact= jieba.cut(files, cut_all=False, HMM=True)    # 精确模式分词+HMM
object_list = []
with open("C:/Users/admin/Desktop/stop.txt", 'r', encoding='UTF-8') as meaninglessFile:   #筛选停用词
    stopwords = set(meaninglessFile.read().split('\n'))
stopwords.add(' ')
for word in seg_list_exact:         # 循环读出每个分词
    if word not in stopwords:       # 如果不在去除词库中
        object_list.append(word)#将清理好的文本放入object_list
word_counts = collections.Counter(object_list)
txtlist=[]
with open("C:/Users/admin/Desktop/dict.txt",encoding="utf-8") as f:
    for txt in f.readlines():
        if txt!=None:
            txtlist.append(txt.strip('\n'))
counts={}
for words in object_list:
    if words in txtlist:
        counts[words] = counts.get(words, 0) + 1  # 逐行写入str格式数据
sql = "insert into medicien(name,id) values (%s,%s)"
for i in counts:
    name = str(i)
    id = counts[i]
    cursor.execute(sql, (name, id))
    cnn.commit()
cursor.close()
cnn.close()
