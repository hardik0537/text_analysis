# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 14:51:57 2018

@author: Hardik Galiawala
"""
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA, TruncatedSVD
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

data = pd.read_csv('train.txt', sep = '\t', header = None)
np_data = data.values
distinct_langs = np.unique(np_data[:, 1])

print(distinct_langs.shape)
subsample_X = np_data[1, :]
start = 0
end = 300
for lang in distinct_langs:
    data_lang = np_data[np_data[:, 1] == lang]
    for i in range(start, end):
        subsample_X = np.concatenate((subsample_X, data_lang[i, :]))
    start = end
    end = end + 300

subsample_X = subsample_X.reshape(int(subsample_X.shape[0]/2),2)
X = subsample_X[:, 0]
y = subsample_X[:, 1]



vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(X)

svd = TruncatedSVD(n_components = 14)
X_svd = svd.fit(X_vectorized).transform(X_vectorized)  

print(X_svd.shape)
print(y.shape)

df = pd.DataFrame({'X1':X_svd[:,0],'X2':X_svd[:,1], 'X3':X_svd[:,2], 'X4':X_svd[:,3],
                   'X5':X_svd[:,4], 'X6':X_svd[:,5], 'X7':X_svd[:,6], 'X8':X_svd[:,7],
                   'X9':X_svd[:,8], 'X10':X_svd[:,9], 'X11':X_svd[:,10], 'X12':X_svd[:,11],
                   'X13':X_svd[:,12], 'X14':X_svd[:,13],
                   'y':y})
sns.set(style="ticks")

sns.pairplot(df, hue = "y")