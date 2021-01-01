from db_tools_jp import db_tools
from divide import divide
import math
import datetime
import pickle
import jieba

jieba.initialize()
db = db_tools()

db.connect()

dv = divide()

start_time = datetime.datetime.now()
contents = db.read_table('news_data')
#[(doc_id,'title','contents','source','time_capture','time_publish')...]
db.close()
N = len(contents)

end_time = datetime.datetime.now()
print(end_time - start_time)
L_AVE = 0
for item in contents:
    try:
        L_AVE += len(item[1] + item[2])
    except BaseException as e:
        pass
L_AVE = L_AVE / N

K1 = 1.5
K3 = 1.4
B = 0.75


#to-do alt function
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


def cal_score(query, score_dict):
    doc_dict = {}
    for term in query:
        if not score_dict.__contains__(term):
            continue
        for item in score_dict[term].items():
            if not doc_dict.__contains__(item[0]):
                doc_dict[item[0]] = item[1]
            else:
                doc_dict[item[0]] += item[1]

    doc_list = sorted(doc_dict.items(), key=lambda item: item[1], reverse=True)
    return doc_list
    #doc_list: [(doc_id,score)...]


#doc_dict{term:[id,tf,score]...}
score_dict = {}
idf_dict = {}
df_dict = {}
adf_dict = {}

score_list = []

word = []
# idf_dict = {}
start_time = datetime.datetime.now()
for item in contents:
    word = dv.stop_word(dv.divide(item[2] + item[2] + item[2] + item[3]))
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
    word = dv.stop_word(dv.divide(item[2] + item[2] + item[2] + item[3]))
    word_dict_doc = {}
    
    id = item[0]
    
    #doc_id id

    for word_item in word:
        df_generater(word_dict_doc, word_item)
    
    #calculate score
    
    for (key, value) in word_dict_doc.items():
        idft = math.log(N / adf_dict[key])
        tftd = 1 + math.log(value)
        ld = len(item[3] + item[2])
        score = idft * ((K1 + 1) * tftd) / (K1 * (
            (1 - B) + B *
            (ld / L_AVE)) + tftd) * (K3 + 1) * tftd / (K3 + tftd)
        # word_dict_doc[key].append(score)
        tfidf = idft * tftd
        hash_tools(idf_dict, {
            # 'term' : str(id),
            'term' : id,
            'doc_id' : key,
            'score' : tfidf
        })
        hash_tools(score_dict, {
            # 'term': str(key),
            # 'doc_id': str(id),
            'term' : key,
            'doc_id' : id,
            'score': score
        })
            # dict_temp = {'term': key, 'doc_id': id, 'score': score}

            # score_list.append(dict_temp)

        # for (key, value) in word_dict_doc:

    # except BaseException as e:

    #     print(e)
    #     pass

#contents = []  #Release memory
#'int' object is not callable
end_time = datetime.datetime.now()
print(end_time - start_time)
start_time = datetime.datetime.now()

with open('idf_dict.index','wb') as f:
    pickle.dump(idf_dict, f, pickle.HIGHEST_PROTOCOL)
with open('score_dict.index', 'wb') as f:
    pickle.dump(score_dict, f, pickle.HIGHEST_PROTOCOL)
with open('term.data','wb') as f:
    pickle.dump(list(df_dict.keys()), f, pickle.HIGHEST_PROTOCOL)
end_time = datetime.datetime.now()
print(end_time - start_time)
# f = open('score.index', 'w')
# pickle.dump(score_dict, f, pickle.HIGHEST_PROTOCOL)
# f.close()
