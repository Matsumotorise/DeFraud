#!/usr/bin/env python
import sys
print(sys.path)
from utils.Utils import Utils

block = Utils.queryMostRecentBlock().json()
transactions = block['Transactions']
for transaction in transactions:
    if transaction['TransactionType'] == 'BASIC_TRANSFER':
        print(transaction['Outputs'][0]['PublicKeyBase58Check'])
        print(Utils.queryProfile(transaction['Outputs'][0]['PublicKeyBase58Check']))





