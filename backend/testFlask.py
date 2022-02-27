#!/usr/bin/env python
import math
import pprint
import sys
from utils.Utils import Utils
import deso
from sklearn import preprocessing
import pickle
import json

from flask import Flask, jsonify, render_template, request
app = Flask(__name__)


# Things needed:
# Search functionality

with open('model.pkl', 'rb') as f:
    clf2 = pickle.load(f)

def run_model(x):
    f = preprocessing.normalize([x], norm='l2')
    return clf2.predict(f)

# Returns {PubKeys[], Usernames[], ProfilePictures[]}
@app.route('/transactionDetails')
def transactionDetails():
    results = {}
    tnxKey = int(request.values.get('transactionKey'))

    input_trans = Utils.queryUserTransaction(tnxKey).json()
    input_trans = input_trans['Transactions'][0]
    print(input_trans)





# int depth
@app.route("/blockDetails/", methods = ['POST'])
def blockDetails():
    n = int(request.values.get('depth'))
    results = {}

    block = Utils.queryMostRecentBlock().json()
    # Get offset if necessary
    if n != 0:
        block = Utils.queryBlock(block["Header"]["Height"]-n).json()
    timeStamp = block["Header"]["TstampSecs"]
    for trans in block['Transactions']:
        if trans['TransactionType'] == 'BASIC_TRANSFER':
            max_received = -math.inf
            min_received = math.inf
            average_received = 0
            n1 = 0
            tID = trans['TransactionIDBase58Check']
            for input_transaction in trans['Inputs']:
                input_trans = Utils.queryUserTransaction(input_transaction['TransactionIDBase58Check']).json()
                input_trans = input_trans['Transactions'][0]['TransactionMetadata']
                max_received = max(max_received, input_trans['BasicTransferTxindexMetadata']['TotalOutputNanos'])
                min_received = min(min_received, input_trans['BasicTransferTxindexMetadata']['TotalOutputNanos'])
                average_received = average_received + input_trans['BasicTransferTxindexMetadata']['TotalOutputNanos']
                n1 += 1
            average_received = average_received / n1

            sent_tnx = len(trans['Inputs'])
            received_tnx = len(trans['Outputs'])

            sum_sent = 0
            min_sent = math.inf
            max_sent = -math.inf
            n = 0
            for out in trans['Outputs']:
                min_sent = min(min_sent, out['AmountNanos'])
                max_sent = max(max_sent, out['AmountNanos'])
                sum_sent = sum_sent + out['AmountNanos']
                n += 1
            avg_sent = sum_sent / n

            total_sent = trans['TransactionMetadata']['BasicTransferTxindexMetadata']['TotalInputNanos']
            total_received = trans['TransactionMetadata']['BasicTransferTxindexMetadata']['TotalOutputNanos']
            balance = total_received - total_sent + trans['TransactionMetadata']['BasicTransferTxindexMetadata']['FeeNanos']
            x = [sent_tnx, received_tnx, min_received/1e9, max_received/1e9, average_received/1e9, min_sent/1e9, max_sent/1e9, avg_sent/1e9, total_sent/1e9, total_received/1e9, balance/1e9]
            print(run_model(x)[0])
            results[tID] = {"timeStamp":timeStamp, "susFlag":int(run_model(x)[0])}
    print(results)
    return jsonify(results)





if __name__ == '__main__':
   app.run()
