import requests
import deso
API_URL = "https://node.deso.org/api/v1"
API_HEADER = {"Content-Type: application/json"}

class Utils:
    # Makes a call to the Dezos chain and retrieves N most recent blocks
    @staticmethod
    def queryLastNBlocks(n):
        pass

    # Post request to get block at height h
    @staticmethod
    def queryBlock(h):
        payload = {"Height": h, "FullBlock": True}
        return requests.post(f"{API_URL}/block", data=payload)

    # Gets user's transactions
    @staticmethod
    def queryUser(pubKey):
        payload = {"PublicKeyBase58Check":pubKey}
        return requests.post(f"{API_URL}/transaction-info", data=payload)

    @staticmethod
    def queryProfile(pubKey):
        payload = {"Username":'e'}
        #print(deso.Users.getProfilePic(pubKey))
        prof = deso.Users.getSingleProfile(pubKey)
        #print(prof['Profile'])
        #transactions = deso.Users.getTransactionInfo(publicKey=pubKey)
        #print(transactions)
        #print(deso.Users.getNotifications(publicKey= pubKey))
        print(deso.Posts.getHiddenPosts(pubKey))
        #print(deso.Posts.getUserPosts(prof['Profile']['Username']))
    # Gets the most recent block (useful for getting height of most recent)
    @staticmethod
    def queryMostRecentBlock():
        return requests.get(API_URL)

    
