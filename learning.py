import arff, numpy as np
import sklearn
import sklearn.linear_model
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score

# Data preparation
dataset = arff.load(open('./combined_binned_norev.arff', 'rb'))
data = np.array(dataset['data'])

data = sklearn.utils.shuffle(data)

num_attr = len(data[0]) - 1
attr = data[:,:num_attr].astype(float)
attr = preprocessing.normalize(attr) # Normalize helps kNN, MLP, seems to hurt perceptron
labels = data[:,num_attr]
le = preprocessing.LabelEncoder()
le.fit(labels)
newlabels = le.transform(labels)

# Sklearn Perceptron
m1 = sklearn.linear_model.Perceptron()
scores = cross_val_score(m1, attr, newlabels, cv=10)
print("Perceptron: {}".format(scores.mean()))

# Sklearn kNN
import sklearn.neighbors
m2 = sklearn.neighbors.KNeighborsClassifier(n_neighbors=45, weights='distance')
scores = cross_val_score(m2, attr, newlabels, cv=10)
print("kNN: {}".format(scores.mean()))

# Sklearn MLP
import sklearn.neural_network
m3 = sklearn.neural_network.MLPClassifier(solver='lbfgs', activation='logistic')
scores = cross_val_score(m3, attr, newlabels, cv=10)
print("MLP: {}".format(scores.mean()))

# Sklearn DT
import sklearn.tree
m4 = sklearn.tree.DecisionTreeClassifier()
scores = cross_val_score(m4, attr, newlabels, cv=10)
print("DT: {}".format(scores.mean()))

#### Ensembles ####

# Ada boost
import sklearn.ensemble
model = sklearn.ensemble.AdaBoostClassifier()
scores = cross_val_score(model, attr, newlabels, cv=10)
print("ADA-Boost: {}".format(scores.mean()))

# Bagging
model = sklearn.ensemble.BaggingClassifier(n_jobs=-1, n_estimators=15)
scores = cross_val_score(model, attr, newlabels, cv=20)
print("Bagging: {}".format(scores.mean()))

# Extra trees
model = sklearn.ensemble.ExtraTreesClassifier(n_estimators=10, n_jobs=-1)
scores = cross_val_score(model, attr, newlabels, cv=20)
print("Extra trees: {}".format(scores.mean()))

# Extra trees
model = sklearn.ensemble.RandomForestClassifier(n_jobs=-1)
scores = cross_val_score(model, attr, newlabels, cv=10)
print("Random Forest: {}".format(scores.mean()))

