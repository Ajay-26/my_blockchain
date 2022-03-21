import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import hashlib
import uuid
from util import *

class Transaction:
	def __init__(self,sender,recipient, amount):
		#For the sake of storage we will store the sender and recipient as their unique ids
		self.sender = sender
		self.recipient = recipient,
		self.amount = amount

class Block:
	def __init__(self, prev_block_hash, transaction_list, test_bits = 2, num_transactions = 1):
		self.prev_block_hash = prev_block_hash
		self.transaction_list = transaction_list
		self.nonce = 0
		self.block_data = " - ".join(self.transaction_list) + self.prev_block_hash
		self.test_bits = test_bits
		self.num_transactions = num_transactions
		#self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()

	def test_condition(self, input_digest):
		#Check if the initial self.test_bits are all 0s
		if(input_digest[:self.test_bits] == '0'*self.test_bits):
			return true
		else:
			return false

	def add_transaction(self, transaction):
		if(len(self.transaction_list) + 1 >= self.num_transactions):
			print("Transaction Limit reached, please create a new block")
			return 0
		else:
			self.transaction_list.append(transaction)
			return 1

	def mine_nonce(self, mine_limit = 1000000):
		for nonce in range(mine_limit):
			if(test_condition(hashlib.sha256((self.block_data + nonce).encode()).hexdigest()) == true):
				self.nonce = nonce
				return
			else:
				pass
		print("Nonce not found, resetting nonce to 0")
		return 

class User:
	def __init__(self,name):
		self.user_id = uuid.uuid4()
		self.name = name

	def change_name(self,new_name):
		self.name = new_name

	def make_transaction(self, blockchain, target_user, amount):
		target_uid = find_user(blockchain, target_user)
		new_transaction = Transaction(self.user_id, target_uid,amount)
		blockchain


class BlockChain(Block):
	def __init__(self):
		self.chain = []
		self.users = []

	def add_users(self, new_username):
		new_user = User(new_username)
		self.users.append(new_user)
		return

	def add_block(self, transaction_list):
		if len(self.chain) == 0:
			prev_hash = 0
		else:
			prev_hash = self.chain[-1].prev_block_hash
		new_block = Block(prev_hash,transaction_list)
		print("Mining....")
		new_block.mine_nonce()
		print("Mining Complete!")
		self.chain.append(new_block)
		return

	def add_transaction(self, transaction):
		if(self.chain[-1].add_transaction(transaction) == 0): #If it is not 0 then the transaction has been added
			transaction_list = []
			transaction_list.append(transaction)
			self.add_block(transaction_list)
			return

