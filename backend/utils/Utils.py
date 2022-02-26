import requests
import deso
import hashlib
import binascii
import base58

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

    # Returns None if it's not safe to access, else the value
    @staticmethod
    def safeMapAccess(m, k):
        if k in m:
            return m[k]
        return None

    # Encryption stuff -------------------------------------------------------
    @staticmethod
    def doubleSha256(hex):
        bin = binascii.unhexlify(hex)
        hash = hashlib.sha256(bin).digest()
        hash2 = hashlib.sha256(hash).digest()
        return str(binascii.hexlify(hash2))

    @staticmethod
    def keyTo58Sum(key, prefix):
        ascii = prefix+key
        hex = binascii.hexlify(bytes(ascii,"utf-8"))
        dSha256 = Utils.doubleSha256(hex)[:4]

        tmp = bytearray()
        tmp.extend(bytearray(prefix.encode('utf-8')))
        tmp.extend(bytearray(key.encode('utf-8')))
        tmp.extend(bytearray(dSha256.encode("utf-8")))
        return base58.b58encode(tmp)

'''
        tmp = bytearray()
        tmp.extend(bytearray(prefix.encode('utf-8')))
        tmp.extend(bytearray(key.encode('utf-8')))
        tmp.extend(bytearray(hash2))
        return base58.b58encode(tmp)
        '''

















