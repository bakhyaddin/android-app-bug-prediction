import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score

df = pd.read_csv("./labelled/combined.csv", index_col=["name"])

versions = [2.1, 2.3, 2.8, 2.9, 2.11, 2.12, 2.13, 2.14, 2.15]

columns_to_drop = ["dit", "noc", "ca", "mfa", "ic", "cbm", "moa"]

# drop columns which have the value of 0
for col in columns_to_drop:
    df.drop([col], inplace=True, axis=1)

# def combinee_csv():
#     combined_csv = pd.concat([pd.read_csv("./labelled/" + str(f) + ".csv") for f in versions])
#     combined_csv.to_csv("./labelled/combined.csv", index=False)

# combinee_csv()

def get_important_features(X, y):

    forest = DecisionTreeClassifier()

    forest.fit(X, y)
    importances = forest.feature_importances_
    indices = np.argsort(importances)[::-1]

    print("Feature ranking:")

    for f in range(X.shape[1]):
        print("%d. feature %s (%f)" % (f + 1, X.columns[f], importances[indices[f]]))

def train_test(X_train, X_test, y_train, y_test, clf, metrics, scores):
    clIndex = 0
    for cl in clf:
        cl.fit(X_train, y_train)
        y_pred = cl.predict(X_test)
        metric_index = 0
        for x in metrics:
            if metric_index == 1:
                score = x(y_test, y_pred)
            else:
                score = x(y_test, y_pred, zero_division=1)
            scores[clIndex][metric_index].append(score)
            metric_index += 1
        clIndex += 1
    print(scores)



clf = [DecisionTreeClassifier(), RandomForestClassifier(), LogisticRegression(max_iter=1000, solver='liblinear'), svm.SVC()]
metrics = [precision_score, accuracy_score, recall_score]

for index in range(len(versions)):
    decisionTreeScores = [[], [], []]
    randomForestScores = [[], [], []]
    logisticsRegressionScores = [[], [], []]
    svmScores = [[], [], []]

    scores = [decisionTreeScores, randomForestScores, logisticsRegressionScores, svmScores]
    if index == len(versions) - 1:
        break
    train = versions[:index + 1]
    test = versions[index + 1]
    df_train = df[df.version.isin(train)]
    df_test = df[df.version == test]

    train_test(df_train.drop(["is_Bug", "version"], axis=1),
                  df_test.drop(["is_Bug", "version"], axis=1),
                  df_train["is_Bug"],
                  df_test["is_Bug"],
                  clf,
                  metrics,
                  scores)

    if versions[index + 1] == versions[-1]:
        get_important_features(df.drop(["is_Bug", "version"], axis=1), df["is_Bug"])
