from IREngine.tools.jieba_ir import jieba
import re


class divide():
    def __init__(self):
        self.re_sc = re.compile(r'[^\u4e00-\u9fa5^0-9^a-z^A-Z]')
        self.d = {}
        stop_word_dict = open('IREngine/tools/cn_stopwords.txt', 'r', encoding='utf-8')
        self.words = stop_word_dict.readlines()
        for item in self.words:
            self.d[item.strip()] = 1
        stop_word_dict.close()

    # regex
    def handle_truple(self, contents):
        content = []
        try:
            for item in contents:
                contents.append(item[0])

        except BaseException as e:
            print("\nerror: ", e)
        return content

    def divide(self, text):
        text_divide = jieba.cut_for_search(re.sub(self.re_sc, '', text))
        word = []
        for item in text_divide:
            word.append(item.lower())
        return word

    def stop_word(self, word):
        word1 = []
        for item in word:
            if not self.d.__contains__(item):
                word1.append(item)
        return word1
