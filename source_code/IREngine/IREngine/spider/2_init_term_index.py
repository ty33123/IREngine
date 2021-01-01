from db_tools_jp import db_tools
from divide import divide
import math
import datetime
import pickle
import jieba
jieba.initialize()
dv = divide()
word_vector = []
k = 19
def dict_term_docid(doc_dict, key, value):
    if not doc_dict.__contains__(key):
        doc_dict[key] = [value, 1]
    else:
        doc_dict[key][1] += 1


def df_generater(df_dict, term):
    if not df_dict.__contains__(term):
        df_dict[term] = 1
    else:
        df_dict[term] += 1


def hash_tools(index_dict, record):

    # index_dict[record[0]][record[1]]=record[2]
    #record  {'term': key, 'doc_id': id, 'score': score}
    if not index_dict.__contains__(str(record['term'])):
        index_dict[str(record['term'])] = {record['doc_id']: record['score']}
    else:
        index_dict[str(record['term'])][record['doc_id']] = record['score']

def top_k(top_term):
    vector = []
    if k>len(top_term):
        for item in top_term:
            vector.append([item[0],item[1]])
    else:
        for index in range(k):
            vector.append([top_term[index][0],top_term[index][1]])
    return vector

# def top_k(top_term):
#     vector = []
    
#     for item in top_term:
#         vector.append([item[0],item[1]])
    
#     return vector
# m=0

def vector_dot(vector1, vector2):
    sum = 0
    #list

    for item1 in vector1:
        for item2 in vector2:
            if item1[0]==item2[0]:
                sum += item1[1]*item2[1]
    
    
    #dict
    #  for key in vector1.keys():
    #     if vector2.__contains__(key):
    #         sum += vector1[key]*vector2[key]
    return sum

def vector_len(vector1):
    sum=0
    for item1 in vector1:
        sum+=item1[1]*item1[1]
    return math.sqrt(sum)

idf_dict = {}

db = db_tools()

db.connect()



start_time = datetime.datetime.now()
contents = db.read_table('search_history')
#[(id,'search_content',null,'time')...]
db.close()
N = len(contents)

end_time = datetime.datetime.now()
print(end_time - start_time)
score_dict = {}

df_dict = {}
adf_dict = {}

score_list = []

word = []
# idf_dict = {}
start_time = datetime.datetime.now()
for item in contents:
    word = dv.stop_word(dv.divide(item[1]))
    df_dict_doc = {}
    for term in word:
        df_generater(df_dict, term)
        df_generater(df_dict_doc, term)
    for item in df_dict_doc.keys():
        if adf_dict.__contains__(item):
            adf_dict[item] += 1
        else:
            adf_dict[item] = 1
for item in contents:

#item
    word = dv.stop_word(dv.divide(item[1]))
    word_dict_doc = {}
    for word_item in word:
        df_generater(word_dict_doc, word_item)

    for (key, value) in word_dict_doc.items():
        idft = math.log(N / adf_dict[key])
        tftd = value

        # word_dict_doc[key].append(score)
        tfidf = idft * tftd
        hash_tools(idf_dict, {
            # 'term' : str(id),
            'term' : item[1],
            'doc_id' : key,
            'score' : tfidf
        })
term_list= []
for item in idf_dict.items():
#item ('1', {'小米': 10.32385113253537...})
# id = int(item[0])

    top_term = sorted(item[1].items(), key=lambda item:item[1], reverse=True)
# print(top_term)

    word_vector.append(top_k(top_term))
    term_list.append(item[0])

with open('idf_dict_term_recom.pickle','wb') as f:
    pickle.dump(word_vector, f, pickle.HIGHEST_PROTOCOL)
with open('term_list_recom.pickle','wb') as f:
    pickle.dump(term_list, f, pickle.HIGHEST_PROTOCOL)
    



#docid-1作为数索引 得到 次级数组 次级数组中[1]为docid

    
            


# with open('word_vector.piclke','rb') as f:
    # pickle.dump(word_vector, f, pickle.HIGHEST_PROTOCOL)
    # word_vector = pickle.load(f)

