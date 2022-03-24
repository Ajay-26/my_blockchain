import flask
from blockchain import *
from flask import request, json, Flask,jsonify, abort, redirect, url_for, render_template

app = Flask(__name__)
blockchain = BlockChain()

@app.route('/', methods = ['GET'])
def index():
	pagetitle = "Welcome to my Blockchain"
	pageheader = "I have nothing else to do"
	return render_template("index.html", mytitle=pagetitle, mycontent= pageheader)

@app.route('/hi/<name>', methods = ['GET'])
def hi(name):
	return jsonify({'code':200, 'Message': 'Hey {name}, just testing if this works'.format(name=name)})

@app.route('/account/<user>', methods = ['GET','POST'])
def display_account(user):
	if request.method == 'GET':
		title = "Please log into your account"
		return render_template("login.html", page_title=title, method= "login", uid = user)
	elif request.method == 'POST':
		uid = user
		print("Reached Here")
		user = find_user(blockchain,user)
		print(user.balance)
		if(request.form['username'] == user.name and hashlib.sha256(request.form['password'].encode()).hexdigest() == user.password):
			data = {"username" : user.name, "balance" : str(user.balance), "payment_link" : str(request.url) + '/pay'}
			return render_template('account.html', data=data)
			#return jsonify({'code':200, 'Message': 'Username = {u_name}, Coins in account = {acct}'.format(u_name=  user.name, acct = str(user.balance))}) 
		else:
			return jsonify({"Error":"Invalid Login"})

@app.route('/account/<user>/pay', methods = ["GET","POST"])
def pay_user(user):
	if request.method == 'GET':
		return render_template("pay.html", uid= user)
	elif request.method == 'POST':
		password = request.form['password']
		this_user = find_user(blockchain,user)
		if(hashlib.sha256(password.encode()).hexdigest() != this_user.password):
			return jsonify({"Error":"Password Incorrect - Can't make payment"})
		else:
			target_uid = request.form['uid']
			amount = int(request.form['amount'])
			blockchain.make_payment(user,target_uid,amount)
			return redirect(url_for('display_account',user= user))

@app.route('/account', methods = ['GET'])
def show_all_accounts():
	data_dict = {}
	for idx,users in enumerate(blockchain.users):
		data_dict["Username of User {}".format(str(idx))] = users.name
		data_dict["Unique ID of User {}".format(str(idx))] = users.user_id
	return jsonify({"code":200, **data_dict})

@app.route('/create-account', methods = ['GET','POST'])
def create_account():
	if request.method == 'POST':
		username = request.form['username']
		password = hashlib.sha256(request.form['password'].encode()).hexdigest()
		uid = blockchain.add_user(username,password)
		return redirect(url_for('display_account', user = uid))

	elif request.method == "GET":
		title = "Welcome, Please enter your details to create an account"
		return render_template('login.html', page_title=title, method = 'create', uid = "aaa")
