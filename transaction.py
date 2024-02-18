import helpers

class Transaction:
    def __init__(self, receiverPublicKey, senderPublicKey, amount):
        self.amount = amount
        self.receiverPublicKey = receiverPublicKey
        self.senderPublicKey = senderPublicKey
        self.signature = None
    
    def signTransaction(self, privateKey):
        self.signature = helpers.sign(self.getTransactionToString(), privateKey)

    def verifyTransaction(self):
        return helpers.verify_signature(self.getTransactionToString(), self.signature, self.senderPublicKey)
    
    def getTransactionToString(self):
        return str(self.amount) + str(self.receiverPublicKey) + str(self.senderPublicKey)
    
    def getTransactionWithSignature(self):
        return str(self.amount) + str(self.receiverPublicKey) + str(self.senderPublicKey) + str(self.signature)