import arff, numpy as np
import sklearn
import sklearn.linear_model
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score


dataset = arff.load(open('./combined_binned_norev.arff', 'rb'))
data = np.array(dataset['data'])

data = sklearn.utils.shuffle(data)

num_attr = len(data[0]) - 1
attr = data[:,:num_attr].astype(float)
labels = data[:,num_attr]
le = preprocessing.LabelEncoder()
le.fit(labels)
newlabels = le.transform(labels)

# Sklearn Perceptron
model = sklearn.linear_model.Perceptron()
scores = cross_val_score(model, attr, newlabels, cv=10)
print("Perceptron: {}".format(scores.mean()))

# Sklearn kNN
import sklearn.neighbors
model = sklearn.neighbors.KNeighborsClassifier(n_neighbors=10, weights='distance')
scores = cross_val_score(model, attr, newlabels, cv=10)
print("kNN: {}".format(scores.mean()))

# Sklearn MLP
import sklearn.neural_network
model = sklearn.neural_network.MLPClassifier()
scores = cross_val_score(model, attr, newlabels, cv=10)
print("MLP: {}".format(scores.mean()))

# Sklearn DT
import sklearn.tree
model = sklearn.tree.DecisionTreeClassifier()
scores = cross_val_score(model, attr, newlabels, cv=10)
print("DT: {}".format(scores.mean()))
