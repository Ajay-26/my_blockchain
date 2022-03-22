from blockchain import *

blockchain = BlockChain()

name1 = "Ajay"
name2 = "Nivi"

blockchain.add_user(name1)
blockchain.add_user(name2)

id1 = blockchain.users[0].user_id
id2 = blockchain.users[1].user_id

amount = 10

blockchain.make_payment(id1,id2,amount)
blockchain.make_payment(id1,id2,amount)
blockchain.make_payment(id1,id2,amount)
blockchain.make_payment(id1,id2,amount)

print("{name_1}'s balance = {amount}".format(name_1 = name1, amount=blockchain.users[0].balance))
print("{name_2}'s balance = {amount}".format(name_2 = name2, amount=blockchain.users[1].balance))
