#!/usr/bin/env python
import sys
print(sys.path)
from utils.Utils import Utils

block = Utils.queryMostRecentBlock().json()
transactions = block['Transactions']
print(transactions[0])





