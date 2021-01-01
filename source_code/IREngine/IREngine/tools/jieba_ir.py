import jieba
def init():
    jieba.dt.tmp_dir = './'
    jieba.dt.cache_file = 'jieba.temp'
    jieba.dt.initialize()