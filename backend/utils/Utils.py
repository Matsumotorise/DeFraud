import requests
import deso
API_URL = "https://node.deso.org/api/v1"
API_HEADER = {"Content-Type": "application/json; charset=utf-8"}


class Utils:
    # Post request to get block at height h
    @staticmethod
    def queryBlock(h):
        payload = {"Height": h, "FullBlock": True,}
        return requests.post(f"{API_URL}/block", headers=API_HEADER, json=payload)

    # Gets user's transactions
    @staticmethod
    def queryUserTransaction(pubKey):
        return deso.Users.getTransactionInfo(publicKey=pubKey)
        #return requests.post(f"{API_URL}/transaction-info", headers=API_HEADER, json=payload)

    @staticmethod
    def queryProfile(pubKey):
        prof = deso.Users.getSingleProfile(pubKey)
        #print(prof['Profile'])
        return deso.Users.getTransactionInfo(publicKey=pubKey)
        
    # Gets the most recent block (useful for getting height of most recent)
    @staticmethod
    def queryMostRecentBlock():
        return requests.get(API_URL)

    @staticmethod
    def safeMapAccess(m, k):
        if k in m:
            return m[k]
        return None

