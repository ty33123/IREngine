import jieba
#from db_tools import db_tools
import re

re_sc = re.compile(r'[^\u4e00-\u9fa5^0-9^a-z^A-Z]')
d = {}
stop_word_dict = open('cn_stopwords.txt','r',encoding='utf-8')
words = stop_word_dict.readlines()

for item in words:
    d[item.strip()]=1

stop_word_dict.close()



class divide():
    
    #regex
    def handle_truple(self, contents):
        content = []
        try:
            for item in contents:
                contents.append(item[0])

        except BaseException as e:
            print("\nerror: ",e)
        return content

    def divide(self, text):
        # db=db_tools()
        # db.connect()
        #connect MySQL service
        text_divide = jieba.cut_for_search(re.sub(re_sc, '', text))
        word = []
        for item in text_divide:
            word.append(item.lower())
            # 统一归于小写


        return word

    def stop_word(self, word):
        word1=[]
        for item in word:
            if (not d.__contains__(item)):
                word1.append(item)
        return word1

        

# from db_tools_alt import db_tools
# from divide import divide
# db=db_tools()
# db.connect()
# jdk=divide()
# text = db.read_line('news_data','1')
# word=jdk.stop_word(jdk.divide(text))
# print(word)

# db.close()


# strs=["我来到北京清华大学","乒乓球拍卖完了","中国科学院大学"]
# for str in strs:
#     seg_list=jieba.cut(str,cut_all=False)
#     print(" ".join(list(seg_list)))