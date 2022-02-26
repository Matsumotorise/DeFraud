#!/usr/bin/env python
import sys
print(sys.path)
from utils.Utils import Utils

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

    # Track up the chain, and parse data for each user
    for pKeys in userHashes.keys():



    print(userHashes)

'''
block = Utils.queryMostRecentBlock().json()
transactions = block['Transactions']
print(transactions[0])
'''



if __name__ == "__main__":
    main()


