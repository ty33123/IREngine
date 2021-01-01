# -*- coding: utf-8 -*-#
# Name:         recom_query
# Description:
# Author:       王继平
# Date:         2020/12/20


from IREngine.tools.divide import divide
import math
import pickle


class Recom_Query():
    def __init__(self, idf_dict_term, term_list):
        self.word_vector = pickle.load(open(idf_dict_term, 'rb'))
        self.term_list = pickle.load(open(term_list, 'rb'))
        self.dv = divide()

    def dict_term_docid(self, doc_dict, key, value):
        if not doc_dict.__contains__(key):
            doc_dict[key] = [value, 1]
        else:
            doc_dict[key][1] += 1


    def df_generater(self, df_dict, term):
        if not df_dict.__contains__(term):
            df_dict[term] = 1
        else:
            df_dict[term] += 1


    def hash_tools(self, index_dict, record):
        if not index_dict.__contains__(str(record['term'])):
            index_dict[str(record['term'])] = {record['doc_id']: record['score']}
        else:
            index_dict[str(record['term'])][record['doc_id']] = record['score']

    def top_k(self, top_term):
        vector = []
        if 19>len(top_term):
            for item in top_term:
                vector.append([item[0],item[1]])
        else:
            for index in range(19):
                vector.append([top_term[index][0],top_term[index][1]])
        return vector


    def vector_dot(self, vector1, vector2):
        sum = 0
        #list

        for item1 in vector1:
            for item2 in vector2:
                if item1[0]==item2[0]:
                    sum += item1[1]*item2[1]
        return sum

    def vector_len(self, vector1):
        sum=0
        for item1 in vector1:
            sum+=item1[1]*item1[1]
        return math.sqrt(sum)



    def recom_query(self, keywords):
        N = len(self.word_vector)
        sim_list_doc = []
        word = self.dv.stop_word(self.dv.divide(keywords))
        df_dict_doc = {}
        df_dict = {}
        adf_dict = {}
        query_idf_dict = {}
        for term in word:
            self.df_generater(df_dict, term)
            self.df_generater(df_dict_doc, term)
        for item in df_dict_doc.keys():
            if adf_dict.__contains__(item):
                adf_dict[item] += 1
            else:
                adf_dict[item] = 1
        word_dict_doc = {}
        for word_item in word:
            self.df_generater(word_dict_doc, word_item)

        for (key, value) in word_dict_doc.items():
            idft = math.log(N / (adf_dict[key]))
            tftd = value
            # word_dict_doc[key].append(score)
            tfidf = idft * tftd
            self.hash_tools(query_idf_dict, {
                # 'term' : str(id),
                'term' : keywords,
                'doc_id' : key,
                'score' : tfidf
            })
        for item in query_idf_dict.items():
            top_term = sorted(item[1].items(), key=lambda item:item[1], reverse=True)
        query = self.top_k(top_term)
        len_query = len(query)
        for index2 in range(1,N):
            sim_list_doc.append([(self.vector_dot(query, self.word_vector[index2]))/(len_query*len(self.word_vector[index2])), self.term_list[index2]])
        sim_list_doc.sort(reverse=True)
        return [i[1] for i in sim_list_doc[0:5]]



