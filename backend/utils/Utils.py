import requests

API_URL = "https://node.deso.org/api/v1"
API_HEADER = {"Content-Type": "application/json; charset=utf-8"}


class Utils:
    # Post request to get block at height or blockHash h
    @staticmethod
    def queryBlock(h):
        payload = {"Height": h, "FullBlock": True,}
        return requests.post(f"{API_URL}/block", headers=API_HEADER, json=payload)

    # Gets user's transactions
    @staticmethod
    def queryUser(pubKey):
        payload = {"PublicKeyBase58Check" : pubKey,}
        return requests.post(f"{API_URL}/transaction-info", headers=API_HEADER, json=payload)

    # Gets the most recent block (useful for getting height of most recent)
    @staticmethod
    def queryMostRecentBlock():
        return requests.get(API_URL)

    # Returns None if it's not safe to access, else the value
    @staticmethod
    def safeMapAccess(m, k):
        if k in m:
            return m[k]
        return None

