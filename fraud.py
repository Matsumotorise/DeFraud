from traceback import print_tb
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

transaction_data = pd.read_csv('./transaction_dataset.csv')
print(transaction_data.keys())
labels = transaction_data['FLAG']
transaction_data = transaction_data[['FLAG', 'Avg min between sent tnx',\
    'Avg min between received tnx',\
    'Time Diff between first and last (Mins)',\
    'Sent tnx',\
    'Received Tnx',\
    'Number of Created Contracts',\
    'Unique Sent To Addresses',\
    'Unique Received From Addresses',\
    'min value received',\
    'max value received ',\
    'avg val received',\
    'min val sent',\
    'max val sent',\
    'avg val sent',\
    'total Ether sent',\
    'total ether received',\
    'total ether sent contracts',\
    'total ether balance'
    ]]
transaction_data = transaction_data.sample(frac=1).reset_index(drop=True)
transaction_data['total ether balance'] = preprocessing.normalize(transaction_data['total ether balance'], norm='l2')
transaction_data['total ether sent contracts'] = preprocessing.normalize(transaction_data['total ether sent contracts'], norm='l2')
transaction_data['total ether received'] = preprocessing.normalize(transaction_data['total ether received'], norm='l2')
transaction_data['total Ether sent'] = preprocessing.normalize(transaction_data['total Ether sent'], norm='l2')
transaction_data['avg val sent'] = preprocessing.normalize(transaction_data['avg val sent'], norm='l2')
transaction_data['max val sent'] = preprocessing.normalize(transaction_data['max val sent'], norm='l2')
transaction_data['min val sent'] = preprocessing.normalize(transaction_data['min val sent'], norm='l2')
transaction_data['avg val received'] = preprocessing.normalize(transaction_data['avg val received'], norm='l2')
transaction_data['max value received'] = preprocessing.normalize(transaction_data['max value received'], norm='l2')
transaction_data['avg val received'] = preprocessing.normalize(transaction_data['avg val received'], norm='l2')
transaction_data['min value received'] = preprocessing.normalize(transaction_data['min value received'], norm='l2')


train, test = train_test_split(transaction_data, test_size=0.2)
train_targets = train['FLAG'].to_numpy()
train_features = train[['Avg min between sent tnx',\
    'Avg min between received tnx',\
    'Time Diff between first and last (Mins)',\
    'Sent tnx',\
    'Received Tnx',\
    'Number of Created Contracts',\
    'Unique Sent To Addresses',\
    'Unique Received From Addresses',\
    'min value received',\
    'max value received ',\
    'avg val received',\
    'min val sent',\
    'max val sent',\
    'avg val sent',\
    'total Ether sent',\
    'total ether received',\
    'total ether sent contracts',\
    'total ether balance'
    ]].to_numpy()

test_targets = test['FLAG'].to_numpy()
test_features = test[['Avg min between sent tnx',\
    'Avg min between received tnx',\
    'Time Diff between first and last (Mins)',\
    'Sent tnx',\
    'Received Tnx',\
    'Number of Created Contracts',\
    'Unique Sent To Addresses',\
    'Unique Received From Addresses',\
    'min value received',\
    'max value received ',\
    'avg val received',\
    'min val sent',\
    'max val sent',\
    'avg val sent',\
    'total Ether sent',\
    'total ether received',\
    'total ether sent contracts',\
    'total ether balance'
    ]].to_numpy()
clf = LogisticRegression(random_state=0).fit(train_features, train_targets)
print(clf.score(test_features, test_targets))
#for x, y in zip(test_features, test_targets):
#    print(x, y)
