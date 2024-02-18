import helpers
from transaction import Transaction
from wallet import Wallet

class Validator(Wallet):
    def __init__(self, wallet):
        super().__init__()
        self.stakePublicKey, self.stakePrivateKey = helpers.generate_keys()

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

    def getStake(self, blockchain):
        return self.blockchain.getBalanceOfAddress(self.stakePublicKey)