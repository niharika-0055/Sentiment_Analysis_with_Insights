import pandas as pd

df =  pd.read_csv(r'balanced_reviews.csv')



df.isnull().any(axis = 0)

#handle the missing data
df.dropna(inplace =  True)

#leaving the reviews with rating 3 and collect reviews with
#rating 1, 2, 4 and 5 onyl

df = df [df['overall'] != 3]

import numpy as np

#creating a label
#based on the values in overall column
df['Positivity'] = np.where(df['overall'] > 3 , 1 , 0)

#NLP
#reviewText - feature - df['reviewText']
#Positivity - label - df['Positivity']

from sklearn.model_selection import train_test_split

features_train, features_test, labels_train, labels_test = train_test_split(df['reviewText'], df['Positivity'], random_state = 42 )



from sklearn.feature_extraction.text import TfidfVectorizer

vect = TfidfVectorizer(min_df = 5).fit(features_train)


features_train_vectorized = vect.transform(features_train)

#model building

from sklearn.linear_model import LogisticRegression


model = LogisticRegression(solver='lbfgs', max_iter=1000)

model.fit(features_train_vectorized, labels_train)

predictions = model.predict(vect.transform(features_test))


from sklearn.metrics import confusion_matrix

confusion_matrix(labels_test, predictions)

from sklearn.metrics import roc_auc_score
roc_auc_score(labels_test, predictions)


#save - pickle format

import pickle

pickle.dump(model, open("pickle_model_1.pkl","wb"))


#pickle the vocabulary
pickle.dump(vect.vocabulary_, open('features.pkl', 'wb'))

