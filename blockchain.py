import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import hashlib
import json
import uuid
from util import *

class Transaction:
	def __init__(self,sender,recipient, amount):
		#For the sake of storage we will store the sender and recipient as their unique ids
		self.sender = sender
		self.recipient = recipient,
		self.amount = amount

class Block:
	def __init__(self, prev_block_hash, transaction_list, test_bits = 2, num_transactions = 2, mine_limit = 10000000):
		self.prev_block_hash = prev_block_hash
		self.transaction_list = transaction_list
		self.nonce = 0
		print(self.transaction_list, self.prev_block_hash)
		self.block_data = " - ".join((self.transaction_list)) + self.prev_block_hash
		self.test_bits = test_bits
		self.num_transactions = num_transactions
		self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()
		self.mine_limit = mine_limit

	def test_condition(self, input_digest):
		#Check if the initial self.test_bits are all 0s
		if(input_digest[:self.test_bits] == '0'*self.test_bits):
			return 1
		else:
			return 0

	def add_transaction(self, transaction):
		if(len(self.transaction_list) + 1 >= self.num_transactions):
			print("Transaction Limit reached, creating new block")
			return 0
		else:
			self.transaction_list.append(make_transaction_list_elt(transaction))
			return 1

	def mine_nonce(self):
		mine_limit = self.mine_limit
		for nonce in range(mine_limit):
			tmp = hashlib.sha256((self.block_data + str(nonce)).encode()).hexdigest()
			if(self.test_condition(tmp) == 1):
				self.nonce = nonce
				print(tmp)
				self.block_hash = tmp 
				return
			else:
				pass
		print("Nonce not found, resetting nonce to 0")
		return 

class User:
	def __init__(self,name,password = "abc", starting_amount = 100):
		self.user_id = str(uuid.uuid4())
		self.name = name
		self.password = password
		self.balance = starting_amount

	def change_name(self,new_name):
		self.name = new_name

	def make_transaction(self, blockchain, target_user_id, amount):
		target_user = find_user(blockchain, target_user_id)
		new_transaction = Transaction(self.user_id, target_user_id,amount)
		blockchain.add_transaction(new_transaction)
		self.balance = self.balance - amount

class BlockChain(Block):
	def __init__(self, test_bits=4):
		self.chain = []
		self.users = []
		self.test_bits = test_bits

	def add_user(self, new_username, new_password = 'abc'):
		new_user = User(new_username,new_password)
		self.users.append(new_user)
		return new_user.user_id

	def add_block(self, transaction_list):
		if len(self.chain) == 0:
			prev_hash = str(0)
		else:
			prev_hash = str(self.chain[-1].block_hash)
		new_block = Block(prev_hash,transaction_list,self.test_bits)
		print("Mining....")
		new_block.mine_nonce()
		print("Mining Complete!")
		self.chain.append(new_block)
		return

	def add_transaction(self, transaction):
		if(len(self.chain) == 0):
			t_list = []
			t_list.append(make_transaction_list_elt(transaction))
			self.add_block(t_list)
		if(self.chain[-1].add_transaction(transaction) == 0): #If it is not 0 then the transaction has been added
			transaction_list = []
			transaction_list.append(make_transaction_list_elt(transaction))
			self.add_block(transaction_list)
			return

	def make_payment(self, user_id1, user_id2, amount):
		#Make user_id1 pay user_id2 amount coins
		user1 = find_user(self,user_id1)
		user2 = find_user(self,user_id2)
		user1.make_transaction(self,user_id2,amount)
		user2.balance = user2.balance + amount


