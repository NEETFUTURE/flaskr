#coding:utf_8
import sqlite3
from flask import Flask, render_template, url_for, request, session, g, redirect, abort, flash
from contextlib import closing, contextmanager
from gef import makexml
import sys
import socketUdp
import datetime

#configration
DATABASE = "flaskr.db"
DEBUG = True
SECRET_KEY = 'development key'
SW = ":|:" #Word to separate 
#USERNAME = 'admin'
#PASSWORD = 'default'

#create application
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()

def today_data():
	d = datetime.datetime.today()
	return d.stream("%x %X")

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	g.db.close()

@app.route('/')
def show_entries():
	sql = """
		select id, username, text
		from entries
		order by id desc
		;"""
	cur = g.db.execute(sql)
	entries = [dict(id=t0, username=t1, text=t2) for t0, t1, t2 in cur.fetchall()]
	g.db.commit()
	if not session.get('username'):
		return render_template('show_entries.html', entries=entries)
	
	return render_template('show_entries.html', entries=entries, username = session['username'])

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('username'):
		abort(401)
	sql="""
	insert into entries(username, text)
	values(?,?)
	;"""
	g.db.execute(sql, [request.form['username'], request.form['text']])
	g.db.commit()
	#a = makexml("Flask",uname=request.form['username'])
	#print a
	
	#Use socket 
	sock = socketUdp.useUdp()
	sock.sendData(SW + "Flask" + SW + request.form['username'] + SW + request.form['text'])
	sock.closeSocket()
	
	flash('new entry was successfully posted')
	return redirect(url_for('show_entries'))


@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
	error= None
	sql = """
		insert into users(username, pass)
		values(?,?)
		;"""
	if request.method == 'POST':
		if request.form['username'] == "":
			error = 'input something'
		elif request.form['password'] == "":
			error = 'input something'
		else:
			#session['logged_in'] = True
			session['username'] = request.form['username']
			g.db.execute(sql, [request.form['username'], request.form['password']])
			g.db.commit()
			flash('new account was successfully')
			return redirect(url_for('show_entries'))		
	return render_template('sign_up.html',error=error)


@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	sql = """
		select username, pass
		from users
		order by id desc
		;"""
	
	cur = g.db.execute(sql)
	entries = [dict(username=t1, password=t2) for t1, t2 in cur.fetchall()]
	
	if request.method == 'POST':
		for i in entries:
			if i['username'] == (request.form['username']):
				if i["password"] == request.form['password']:
					#session['logged_in'] = True
					session['username'] = request.form['username']
					print session['username']
					flash('You were logged in')
					g.db.commit()
					return redirect(url_for('show_entries'))
				else:
					error = 'invalid pass'
		error = 'invalid = username' 
		g.db.commit()
		return render_template('login.html', error=error)
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('username', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))

@app.route('/backdoor')
def backdoor():
	pass
	
if __name__ == '__main__':
	app.run()



