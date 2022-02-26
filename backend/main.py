#!/usr/bin/env python
import sys
print(sys.path)
from utils.Utils import Utils
import deso
from sklearn import preprocessing
import pickle

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
def main():
    # Make a call to the Dezos chain and retrieves N most recent blocks
    maxHeight = Utils.queryMostRecentBlock().json()['Header']['Height']

    # End up with a list of Publickey : [t1, t2, ...]
    # Where t1, t2, ... are transactions of the form {time, transferAmt, transactionKey, to/fromKey} (If transferAmt positive, then it's fromKey, if negative, it's toKey)

    userHashes = {}
    n=5

    # Get each block and parse info here
    for i in range(maxHeight-n, maxHeight):
        try:
            data = Utils.queryBlock(i).json()
        except:
            print(f"WARN: something went wrong trying to query block {i}")
            continue

        header = Utils.safeMapAccess(data, 'Header')
        if header == None:
            print(f"WARN: something went wrong trying to query block {i} @header")
            continue

        time = Utils.safeMapAccess(header, 'TstampSecs')
        if time == None:
            print(f"WARN: something went wrong trying to query block {i} @Time")
            continue

        #(TODO: )
        # Where t1, t2, ... are transactions of the form dict{time, transferAmt, transactionKey, to/fromKey} (If transferAmt positive, then it's fromKey, if negative, it's toKey)
        # Having an issue identifying to/from with transaction data alone
        t = {"time" : time}

        # Extract public hashes out of blocks
        transactions = Utils.safeMapAccess(data, 'Transactions')
        if transactions == None:
            print(f"WARN: something went wrong trying to query block {i} @Transactions")
            continue

        for t in transactions:
            metaData = Utils.safeMapAccess(t, 'TransactionMetadata')
            if(metaData == None):
                print(f"WARN: something went wrong trying to query block {i} @Metadata")
                continue

            affectedKeys = Utils.safeMapAccess(metaData, 'AffectedPublicKeys')
            if(affectedKeys == None):
                print(f"WARN: something went wrong trying to query block {i} @AffectedKeys")
                continue

            for ak in affectedKeys:
                curK = ak['PublicKeyBase58Check']
                if curK not in userHashes:
                    userHashes[curK] = [ak['Metadata']]
                else:
                    userHashes[curK].append(ak['Metadata'])
    import math
    max_sent = -math.inf
    min_sent = math.inf
    sum_sent = 0
    n1 = 0
    block = Utils.queryMostRecentBlock().json()
    for trans in block['Transactions']:

        if trans['TransactionType'] == 'BASIC_TRANSFER':
            n1 = n1 + 1
            print(trans)
            sum_sent = sum_sent + trans['Outputs'][0]['AmountNanos']
            min_sent = min(min_sent, trans['Outputs'][0]['AmountNanos'])
            max_sent = max(max_sent, trans['Outputs'][0]['AmountNanos'])
            sent_tnx = len(trans['Inputs'])
            received_tnx = len(trans['Outputs'])
            import math
            min_received = math.inf
            max_received = -math.inf
            sum_received = 0
            n = 0
            for out in trans['Outputs'][1:]:
                min_received = min(min_received, out['AmountNanos'])
                max_received = max(max_received, out['AmountNanos'])
                sum_received = sum_received + out['AmountNanos']
                n = n + 1
            avg_received = sum_received / n

            total_sent = trans['TransactionMetadata']['BasicTransferTxindexMetadata']['TotalInputNanos']
            total_received = trans['TransactionMetadata']['BasicTransferTxindexMetadata']['TotalOutputNanos']
            balance = total_received - total_sent + trans['TransactionMetadata']['BasicTransferTxindexMetadata']['FeeNanos']
            x = [sent_tnx, received_tnx, min_received, max_received, avg_received, min_sent, max_sent, sum_sent/ n1, total_sent, total_received, balance]
            print(run_model(x))
'''
    # Track up the chain, and parse data for each user
    for pKeys in userHashes.keys():



    print(userHashes)

>>>>>>> c6817ca42e1ec8c5c38b00d9fc6af7ae469f8009
'''

'''
block = Utils.queryMostRecentBlock().json()
transactions = block['Transactions']
print(transactions[0])
'''



if __name__ == "__main__":
    main()


