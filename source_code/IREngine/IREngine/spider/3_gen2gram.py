# -*- coding: utf-8 -*-#
# Name:         gen2gram
# Description:  
# Author:       刘天昀
# Date:         2020/12/13

import pickle

term = pickle.load(open("term.data", "rb"))
gram_index = {}
for t in term:
    temp = "$" + t + "$"
    for w in range(len(temp) - 1):
        n_t = temp[w:w + 2]
        if gram_index.__contains__(n_t):
            gram_index[n_t].append(t)
        else:
            gram_index[n_t] = [t]
pickle.dump(gram_index, open("gram.index","wb"))
