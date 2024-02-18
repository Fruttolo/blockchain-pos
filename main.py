from blockchain import Blockchain
from wallet import Wallet
import time

wallet1 = Wallet()
wallet2 = Wallet()
wallet3 = Wallet()

blockchain = Blockchain([wallet1, wallet2, wallet3]) # Create a blockchain with the initial validators

for i in range(5):
    print("Wallet 1 balance: " + str(wallet1.getBalance(blockchain)))
    print("Wallet 2 balance: " + str(wallet2.getBalance(blockchain)))
    print("Wallet 3 balance: " + str(wallet3.getBalance(blockchain)))

    print("Wallet 1 staked: " + str(wallet1.getStaked(blockchain)))
    print("Wallet 2 staked: " + str(wallet2.getStaked(blockchain)))
    print("Wallet 3 staked: " + str(wallet3.getStaked(blockchain)))

    wallet1.unstakeMoney(blockchain, 15)
    wallet2.unstakeMoney(blockchain, 20)
    wallet3.unstakeMoney(blockchain, 50)

    transaction1 = wallet1.sendMoney(wallet2.getPublicKey(), 40)
    transaction2 = wallet2.sendMoney(wallet3.getPublicKey(), 10)
    transaction3 = wallet3.sendMoney(wallet1.getPublicKey(), 3)

    blockchain.addTransaction(transaction1)
    blockchain.addTransaction(transaction2)
    blockchain.addTransaction(transaction3)

    blockchain.minePendingTransactions()

    print()

    time.sleep(1)

blockchain.printChain()
print("the chain is valid: " + str(blockchain.isChainValid()))

