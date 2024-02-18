import helpers
from transaction import Transaction

class Wallet:
    def __init__(self):
        self.publicKey, self.privateKey = helpers.generate_keys()
        self.stakePublicKey, self.stakePrivateKey = helpers.generate_keys()

    def sendMoney(self, receiverPublicKey, amount):
        transaction = Transaction(receiverPublicKey, self.publicKey, amount)
        transaction.signTransaction(self.privateKey)
        return transaction

    def getPublicKey(self):
        return self.publicKey
    
    def getBalance(self, blockchain):
        return blockchain.getBalanceOfAddress(self.publicKey)
    
    def getStakePublicKey(self):
        return self.stakePublicKey
    
    def stakeMoney(self, amount):
        transaction = Transaction(self.stakePublicKey, self.publicKey, amount)
        transaction.signTransaction(self.privateKey)
        return transaction

    def unstakeMoney(self, amount):
        transaction = Transaction(self.publicKey, self.stakePublicKey, amount)
        transaction.signTransaction(self.stakePrivateKey)
        return transaction

    def getStaked(self, blockchain):
        return blockchain.getBalanceOfAddress(self.stakePublicKey)