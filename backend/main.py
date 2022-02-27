#!/usr/bin/env python
import deso
import math
import pprint
import sys
from utils.Utils import Utils
from sklearn import preprocessing
import pickle
import json

print(sys.path)
with open('model.pkl', 'rb') as f:
    clf2 = pickle.load(f)

def run_model(x):
    f = preprocessing.normalize([x], norm='l2')
    return clf2.predict(f)

def main2():
    block = Utils.queryMostRecentBlock().json()
    transactions = block['Transactions']
    for transaction in transactions:
        #print(transaction)
        Utils.queryProfile(transaction['Outputs'][0]['PublicKeyBase58Check'])


def transactionDetails(tnxKey):
    results = {}
    results['Pkeys'] = []
    results['Usernames'] = []
    results['ProfilePicURL'] = []
    trans = Utils.queryUserTransaction(tnxKey).json()

    input_trans = trans["Transactions"][0]["Inputs"]
    output_trans = trans["Transactions"][0]["Outputs"]

    '''
    for inp in input_trans:
        results['Pkeys'].append(inp["PublicKeyBase58Check"])
    '''

    for out in output_trans:
        results['Pkeys'].append(out["PublicKeyBase58Check"])

    print(results['Pkeys'])
    i = 0
    n = len(results['Pkeys'])
    while i < n:
        pKey = results['Pkeys'][i]
        print(i,n)
        try:
            x=deso.Users.getSingleProfile(pKey)
            print(x)
            if('error' in x):
                results['Pkeys'].pop(i)
                n-=1
                continue
            print("--------------", x)
            x=x['Profile']['Username']
            print(x)
            results['Usernames'].append(x)
            results['ProfilePicURL'].append(deso.Users.getProfilePic(pKey))
            i+=1
        except Exception as e:
            print(e)
            i+=1
            continue
    return results


# n int
def main(n):
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
            results[tID] = [timeStamp, run_model(x)]
    print(results)
    return results

if __name__ == "__main__":
    print(transactionDetails("3JuETDb8fDqmttC9HXw4bTwv2gbTTzYCpbArpuWb4iFt5EQuyr62xf"))


