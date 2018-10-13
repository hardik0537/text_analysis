# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 12:02:45 2018

@author: Hardik Galiawala
"""
#from pandas_ml import ConfusionMatrix
import seaborn as sns
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier 
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.cross_validation import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA, TruncatedSVD
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

def fit_predict_report(train_x, test_x, train_y, test_y, pipeline, classifier_name):
    parameter_grid = {'selection__k': [200]}

    grid_search = GridSearchCV(pipeline, param_grid = parameter_grid, refit = True)
    
    predict_train = grid_search.fit(train_x, train_y).predict(train_x)
    predict_test = grid_search.predict(test_x)
    print(predict_train)
    print(predict_test)
    print('Confusion matrix for ' + classifier_name + ' (Train v/s test)')
    print('Train :')
    print(confusion_matrix(train_y, predict_train))
    print('Test :')
    ax= plt.subplot()
    sns.heatmap(confusion_matrix(test_y, predict_test), annot=True, ax = ax, fmt = 'g')
    print('Accuracy:-')
    print('Accuracy score for ' + classifier_name + ' (Train v/s test)')
    print(str(accuracy_score(train_y, predict_train)) +' '+ str(accuracy_score(test_y, predict_test)))
    
def main():
    
    train_data = pd.read_csv('train.txt', sep = '\t', header = None)
    np_train_data = train_data.values
    print(np_train_data.shape)
    
    
    X = np_train_data[:, 0]
    y = np_train_data[:, 1]

    test_data = pd.read_csv('test-gold.txt', sep = '\t', header = None)
    np_test_data = test_data.values
    print(np_test_data.shape)
    
    
    test_x = np_test_data[:, 0]
    test_y = np_test_data[:, 1]
    
    print(test_x)
    print(test_y)
    distinct_langs = np.unique(np_train_data[:, 1])
    print(np.unique(np_test_data[:, 1]).shape)
    #bg_data = np_data[np_data[:, 1] == 'bg']
    print(distinct_langs.shape)

    pipeDecisionTree = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('selection', SelectKBest(chi2)),
            ('decision_tree', DecisionTreeClassifier())
            ])
    # Reference for multinomial naive bayes
    #http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html
    pipeNaiveBayes = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('selection', SelectKBest(chi2)),
            ('naive_bayes', MultinomialNB())
            ])
    #Reference for multinomial logistic regression
    # http://dataaspirant.com/2017/05/15/implement-multinomial-logistic-regression-python/
    pipeLogisticReg = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('selection', SelectKBest(chi2)),
            ('log_reg', LogisticRegression(multi_class = 'multinomial', solver = 'newton-cg'))
            ])
    
    pipeLinearSVC = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('selection', SelectKBest(chi2)),
            ('linear_svc', LinearSVC(multi_class = 'ovr'))
            ])
    
    fit_predict_report(X, test_x, y, test_y, pipeDecisionTree, 'DecisionTree')
    fit_predict_report(X, test_x, y, test_y, pipeNaiveBayes, 'NaiveBayes')
    fit_predict_report(X, test_x, y, test_y, pipeLogisticReg, 'LogisticReg')
    fit_predict_report(X, test_x, y, test_y, pipeLinearSVC, 'LinearSVC')
    
main()


