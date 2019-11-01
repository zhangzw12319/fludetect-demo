import numpy as np
import matplotlib.pyplot as plt
import random
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.model_selection import train_test_split

def Simple_GP(data):
    X_train, X_test, Y_train, Y_test = train_test_split(data.X, data.Y, test_size=0.1)
    plt.scatter(X_train, Y_train, marker='o', color='r', label='3', s = 15)
    plt.show()
    gaussian = GaussianProcessRegressor()
    fitting = gaussian.fit(X_train,Y_train)
    prediction = gaussian.predict(X_test)
    plt.scatter(X_test, Y_test, marker='o', color='r', label='3', s=15)
    plt.plot(X_test, prediction)
    plt.show()


def Simple_GP(X_train, X_test, Y_train, Y_test):
    plt.scatter(X_train, Y_train, marker='o', color='r', label='3', s=15)
    plt.show()
    gaussian = GaussianProcessRegressor()
    fitting = gaussian.fit(X_train, Y_train)
    prediction = gaussian.predict(X_test)
    # plt.scatter(X_test, Y_test, marker='o', color='r', label='3', s=15)
    plt.scatter(X_test, Y_test, marker='o', color='r', label='3', s=15)
    plt.plot(X_test, prediction)
    plt.show()

    return prediction
