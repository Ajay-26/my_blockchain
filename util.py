import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import hashlib
import uuid

def find_user(blockchain, uid):
	for user in blockchain.users:
		if uid == user.user_id:
			return user
	print("User corresponding to user id - {uid} not found, returning none".format(uid = uid))
	return None