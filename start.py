# This is a simple flu-detector for twitter tweets.

# from nltk.twitter import Streamer, Twitter, TweetViewer, TweetWriter, credsfromfile
import preProcessing as preP
from preProcessing import Data
import numpy as np
import Simple_GP
import utils
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from sklearn.model_selection import train_test_split
import time

register_matplotlib_converters()
gp_input_dict={}
gp_output_dict={}

# get all paths for dataset(json files)

data = Data()
all_paths = utils.all_path(r"/home/zzw/twitter13")
print(time.asctime(time.localtime(time.time())))
print(all_paths)


# read all of the json files and pack it into a whole dict


for each_path in all_paths:
    print(each_path)
    data.read_json_files(each_path)
    # extract text from the "text" column in each line, and label it
    data.extract_text_and_label()
    print(time.asctime(time.localtime(time.time())))
    print("Data Extracting and Labeling Finished...")

    # use CountVectorizer from sklearn.feature_extraction.text to bagging words(n-gram)
    # data.n_gram()

    # print(time.asctime(time.localtime(time.time())))
    # print("Word Embedding Finished...")

    # use LogisticRegression or svm_basic to train the filter
    # which will be used to automatically filter tweets related to flu

    # utils.LogisticRegression(data)
    # svm_basic(data)

    # print(time.asctime(time.localtime(time.time())))
    # print("Logistic Regression Finished...")

    # Then we will use Gassian Regression(GP or gp) to predict the ILL rate.
    # First we want to get the input data and output label for GP model.
    # In this step, we have to split the input data by its created time and
    # categorize them into different years and different weeks in the year.
    # Format for 'gp_input_dict' : {"2019":{"47":[Num of Related, Total]},...}
    # Format for 'gp_output_dict' : {"2019":{"47":[Weighted ILL rates, Unweighted ILL rates]},...}

    gp_input_dict = preP.split_data_by_time(X=None, Y=data.Y, time=data.time, split_dict=gp_input_dict)
    gp_output_dict = preP.read_CSV("ILINet.csv")

    data.clear_data(


print(gp_input_dict)
print(gp_output_dict)

# bbbbbbbbb


# 'gp_X' : [Arrays of "Related/Total" for each week]
# 'gp_Y_weighted' : [Arrays of weighted ILL rates for each week]
# 'gp_Y_unweighted' : [Arrays of unweighted ILL rates for each week]
# 'gp_information' : [...("2018","53"),("2019","1"),("2019","2"),...]
# 'gp_X_Y_dict' : {"2019":{"47":["Related/Total", Weighted, Unweighted]},...}

gp_X = []
gp_Y_weighted = []
gp_Y_unweighted = []
gp_information = []
gp_X_Y_dict = {}

# to create 'gp_X_Y_dict'
# key1:year
# key2:No. of week in the year

for (key1, value1) in gp_input_dict.items():
    for (key2, value2) in value1.items():
        print(key2, value2)
        gp_X_Y_dict[(key1, key2)] = [value2[0] / value2[1], gp_output_dict[key1][key2][0], gp_output_dict[key1][key2][1]]

print(gp_X_Y_dict)
order = sorted(gp_X_Y_dict)
print("order=", order)

# to create 'gp_X','gp_Y_weighted','gp_Y_unweighted','gp_information'
for key in order:
    gp_X.append(gp_X_Y_dict[key][0])
    gp_Y_weighted.append(gp_X_Y_dict[key][1])
    gp_Y_unweighted.append(gp_X_Y_dict[key][2])
    gp_information.append(key)


print(gp_X)
print(gp_Y_weighted)
print(gp_Y_unweighted)
print(gp_information)


# use sklearn GaussianProcessRegressor to train and test
X_train, X_test, Y_train, Y_test = train_test_split(gp_X, gp_Y_weighted, test_size=0.5)
prediction = Simple_GP.Simple_GP(np.array(X_train).reshape(-1, 1), np.array(gp_X).reshape(-1, 1), np.array(Y_train), np.array(gp_Y_weighted))

print(time.asctime(time.localtime(time.time())))
print("Gaussian Regression Finished...")

# plot it
axe_x = [str(year)+'-'+str(week) for year, week in gp_information ]
print(axe_x)
plt.plot(axe_x, gp_Y_weighted)
plt.plot(axe_x, prediction)
plt.show()










