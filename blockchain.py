import helpers
from transaction import Transaction
from block import Block

class Blockchain:
    def __init__(self, firstValidators = []):
        self.difficulty = 2 # The number of leading zeros that the hash must have
        self.pendingTransactions = [] # Transactions that are not yet in a block
        self.stakingRewars = 10 # The reward for staking a block
        self.validators = firstValidators # The validators that are staking
        self.chain = [self.createGenesisBlock(200)] # The first block in the chain with a reward of 200 for each initial validator


    # Create the first block in the chain
    def createGenesisBlock(self, initailReward):
        initialTransactions = []
        # Create a transaction for each validator
        for validator in self.validators:
            initialTransactions.append(Transaction(validator.getStakePublicKey(), None, initailReward))
        firstValidator = self.validators[0]
        return Block(initialTransactions, "0", "0", firstValidator.getStakePublicKey())
    
    def getLatestBlock(self):
        return self.chain[len(self.chain) - 1]
    
    # Choose the validator with the most stake
    def chooseValidator(self):
        if len(self.validators) == 0:
            return None
        maxStake = 0
        for validator in self.validators:
            if validator.getStaked(self) > maxStake:
                maxStake = validator.getStaked(self)
        for validator in self.validators:
            if validator.getStaked(self) == maxStake:
                return validator
        return None
    
    def minePendingTransactions(self):
        currentValidator = self.getLatestBlock().nextValidatorPublicKey # Get the current validator
        if currentValidator == None:
            print("No validators")
            return
        nextValidator = self.chooseValidator() # Choose the next validator
        # Create a new block with the pending transactions and mine it
        block = Block(self.pendingTransactions, self.getLatestBlock().hash, currentValidator, nextValidator.getStakePublicKey())
        block.mineBlock(self.difficulty)
        self.chain.append(block)
        self.pendingTransactions = [Transaction(currentValidator, None, self.stakingRewars)]

    def stake(self, wallet, amount):
        if wallet.getBalance(self) < amount:
            print("Not enough money to stake")
            return
        transaction = wallet.stakeMoney(amount)
        self.addTransaction(transaction)
        if wallet.getStakePublicKey() not in self.validators:
            self.validators.append(wallet)

    def unstake(self, wallet, amount):
        for validator in self.validators:
            if validator.getPublicKey() == wallet.getPublicKey():
                if validator.getStaked(self) < amount:
                    print("Not enough money to unstake")
                    return
                transaction = validator.unstakeMoney(amount)
                self.addTransaction(transaction)
                if validator.getStaked(self) == 0:
                    self.validators.remove(validator)
                return
        print("Validator not found")

    def addTransaction(self, transaction):
        if transaction.verifyTransaction() == False:
            print("Transaction failed to verify")
            return
        if transaction.amount <= 0:
            print("Transaction failed amount")
            return
        if self.getBalanceOfAddress(transaction.senderPublicKey) < transaction.amount:
            print("Transaction failed balance")
            return
        self.pendingTransactions.append(transaction)

    def getBalanceOfAddress(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.receiverPublicKey == address:
                    balance += transaction.amount
                if transaction.senderPublicKey == address:
                    balance -= transaction.amount
        return balance
    
    def isChainValid(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i - 1]
            if currentBlock.hash != currentBlock.calculateHash():
                return False
            if currentBlock.previousHash != previousBlock.hash:
                return False
            if not currentBlock.hasValidTransactions():
                return False
        return True
    
    def printChain(self):
        for block in self.chain:
            print("Previous Hash: " + block.previousHash)
            print("Transactions: " + block.getTransactionsToString())
            print("Nonce: " + str(block.nonce))
            print("Hash: " + block.hash)
            print("\n")