import json
import re
import utils
import numpy as np
from scipy.sparse import csr_matrix





class Data:
    json_path = ""
    corpus_dict_batch = []  # 把json文件里的所有json对象放在data_dict_array数组里
    text_array = []
    X = []
    Y = []
    size = 0
    keywords = ["flu", "health", "physician", "fever", "cold", "ill", "sick",
              "cough", "sneeze", "tremble", "medicine", "thermometer",
              "illness", "headache", "sore throat"]

    def __init__(self, path=""):
        self.json_path = path
        self.corpus_dict_batch = [] # storing each json file in the corpus(per batch)
        self.size = 0
        self.X = []
        self.Y = []
        self.time = []

    def clear_data(self):
        self.corpus_dict_batch=[]
        self.size = 0
        self.X = []
        self.Y = []
        self.time = []

    def read_json_files(self, if_print=False):
        with open(self.json_path, 'r') as load_f:
            for line in load_f:
                # print(line)
                data_dict = json.loads(line)
                self.corpus_dict_batch.append(data_dict)
        if if_print:
            print(self.corpus_dict_batch)
        self.size = len(self.corpus_dict_batch)
        if if_print:
            print(self.size)

        # Remember to close file!!
        load_f.close()

    def read_json_files(self, path=json_path, if_print=False):
        with open(path, 'r') as load_f:
            for line in load_f:
                try:
                    data_dict = json.loads(line)
                except:
                    print(line)
                self.corpus_dict_batch.append(data_dict)
        if (if_print):
            print(self.corpus_dict_batch)
        self.size = len(self.corpus_dict_batch)
        if (if_print):
            print(self.size)

    def add_label_by_keyword_filtering(self, text):
       """

       :param text:
       :return:
       """
       word_split = text.split()
       for each_word in self.keywords:
           if each_word in word_split:
              return 1

       return 0

    def extract_text_and_label(self):
        """

        :return:
        """
        for each_json_tweet in self.corpus_dict_batch:
            if "text"not in each_json_tweet:continue
            each_text = each_json_tweet["text"]

            #  get rid of url for each text
            re_expression = re.compile(r'https://[a-zA-Z0-9.?/&=:]*|', re.S)
            each_text = re_expression.sub("", each_text)

            # to check out which language is used, choose English only
            # if utils.lang_detect(each_text) != "en":
            #     continue

            # self.text_array.append(each_text)
            # get label for each text, trangforming it to 0 or 1.
            if "ifFluRelated" in each_json_tweet.keys():
                if each_json_tweet["ifFluRelated"]:
                    self.Y.append(1)
                else:
                    self.Y.append(0)
            else:
                self.Y.append(self.add_label_by_keyword_filtering(each_text))

            created_time_str = each_json_tweet["created_at"]
            str_split = created_time_str.split()
            date = int(str_split[2])
            month = utils.get_month(str_split[1])
            year = int(str_split[5])

            # print(str_split[1])
            # print(year, month, date)

            self.time.append((year, month, date))

        # print(self.text_array)
        print(self.Y)

    def n_gram(self):
        from sklearn.feature_extraction.text import CountVectorizer
        vectorizer = CountVectorizer(ngram_range=(1, 3), token_pattern=r'(\w+)')
        # Produce Feature Vector:
        X = vectorizer.fit_transform(self.text_array)
        # use scipy scr_matrix
        self.X = csr_matrix(X)
        print(vectorizer.get_feature_names())

        # Free memory after extracting data
        from sklearn.externals import joblib
        joblib.dump(X.tocsr(), 'dataset.joblib')


def split_data_by_time(X, Y, time, split_dict=None):
    """
    给定训练集
    :param X:训练输入数据(训练集/测试集)数组（暂时没有用到该参数，未来拓展该函数api时用）
    :param Y:01数组，0表示X数组相应位置的tweet与流感有关，1表示与流感无关
    :param time:该数据创建的时间
    :param split_dict: 字典类型，存储每年每周的tweet总条数以及与疾病相关的条数
    :return:字典{"年份"：{"周数",[与流感有关的数据数量,该周数据总数量],...},...}
    """
    if split_dict is None:
        split_dict = {}
    i = 0
    for each_time in time:
        # 通过年月日计算在这一天属于当年的哪一周
        (year, month, date) = each_time
        from datetime import datetime
        str_time = datetime.strptime(str(year) + '-' + str(month) + '-'+str(date), "%Y-%m-%d")
        week = int(str_time.strftime("%W"))
        str_year = str(year)
        str_week = str(week)

        if str_year not in split_dict.keys():
            split_dict[str_year] = {}

        if str_week not in split_dict[str_year].keys():
            split_dict[str_year][str_week] = [0, 0]

        if Y[i]:
            split_dict[str_year][str_week][0] += 1

        split_dict[str_year][str_week][1] += 1

        i += 1

    return split_dict

def read_CSV(path):
    split_dict = {}
    ill_rate_maxtrix=np.loadtxt(path, delimiter=",", skiprows=1, dtype='str', usecols=(2,3,4,5))
    for each_record in ill_rate_maxtrix:
        year = each_record[0]
        week = each_record[1]
        weighted = each_record[2]
        unweighted = each_record[3]
        str_year = str(year)
        str_week = str(week)
        if str_year not in split_dict.keys():
            split_dict[str_year] = {}

        if str_week not in split_dict[str_year].keys():
            split_dict[str_year][str_week] = [float(weighted), float(unweighted)]

    return split_dict




if __name__ == "__main__":
    data = Data(r"C:\Users\lenovo\twitter-files\final.json")
    data.read_json_files()
    data.extract_text_and_label()
    data.n_gram()


    print("testing ILL rate data...")
    print(read_CSV("ILINet.csv"))



# 字典{"年份"：{"周数",[weighted ILL rate, unweighted ILL rate],...},...}