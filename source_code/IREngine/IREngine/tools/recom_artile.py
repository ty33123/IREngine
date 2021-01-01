# -*- coding: utf-8 -*-#
# Name:         recom_artile
# Description:
# Author:       王继平
# Date:         2020/12/20
import pickle
import math


class Recom_Artile():
    def __init__(self, index_file):
        self.idf_dict = pickle.load(open(index_file, "rb"))
        self.word_vector = self.get_word_vector()
        self.N = len(self.word_vector)
        self.len_list = self.get_len_list(self.N)

    def get_len_list(self, N):
        len_list = []
        for index in range(N):
            len_list.append(self.vector_len(self.word_vector[index]))
        return len_list

    def get_word_vector(self):
        word_vector = []
        for item in self.idf_dict.items():
            top_term = sorted(item[1].items(), key=lambda item: item[1], reverse=True)
            word_vector.append(self.top_k(top_term))
        return word_vector

    def top_k(self, top_term):
        vector = []
        if 19 > len(top_term):
            for item in top_term:
                vector.append([item[0], item[1]])
        else:
            for index in range(19):
                vector.append([top_term[index][0], top_term[index][1]])
        return vector

    def vector_dot(self, vector1, vector2):
        sum = 0
        # list
        for item1 in vector1:
            for item2 in vector2:
                if item1[0] == item2[0]:
                    sum += item1[1] * item2[1]
        return sum

    def vector_len(self, vector1):
        sum = 0
        for item1 in vector1:
            sum += item1[1] * item1[1]
        return math.sqrt(sum)

    def recom_artile(self, id):
        sim_list_doc = []
        for index2 in range(self.N):
            if index2 == id:
                sim_list_doc.append([1, index2])
                continue
            """ if index2<index1:
                sim_list_doc.append([sim_list[index2][index1][0], index2])
                continue """
            sim_list_doc.append(
                [(self.vector_dot(self.word_vector[id], self.word_vector[index2])) / (self.len_list[id] * self.len_list[index2]), index2])
        sim_list_doc.sort(reverse=True)
        result = []
        for item in sim_list_doc[1:6]:
            result.append(item[1]+1)
        return result
