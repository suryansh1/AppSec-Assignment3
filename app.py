from flask import Flask, redirect, render_template, request, session, abort, url_for
import os, subprocess
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired
from flask_bcrypt import Bcrypt
from databases import db
from create_app import app_creator

from models import User

app = app_creator()

bcrypt = Bcrypt()

users_dict = {}
# session['logged_in'] = False


class RegistrationForm(FlaskForm):
	uname = StringField("username")
	pword = PasswordField("password")
	two_fa = PasswordField("two_factor_authentication", id='2fa')

class LoginForm(FlaskForm):
	uname = StringField("username")
	pword = PasswordField("password")
	two_fa = PasswordField("two_factor_authentication", id='2fa')

class SpellCheckForm(FlaskForm):
	inputtext = TextAreaField("inputtext")

@app.route("/")
def home():
	return redirect(url_for('spell_check'))

@app.route("/spell_check", methods=['POST', 'GET'])
def spell_check():
	
	if 'username' not in session:
	# if not session.get('logged_in'):
		return redirect(url_for('login'))

	else:

		form = SpellCheckForm()

		if request.method == 'POST':
			inputtext = request.form['inputtext']

			# print(inputtext)

			with open("test.txt",'w', encoding = 'utf-8') as f:
				f.write(inputtext)

			out = subprocess.check_output(["./a.out", "test.txt", "wordlist.txt"])
			
			# processed_output = ",".join(out.decode().split('\n'))
			processed_output = out.decode().replace('\n', ',')

			print(processed_output)

			os.remove("test.txt")

			return "<p id=textout>" + inputtext + "</p> </br> <p id=misspelled>" + processed_output\
					+"</p>"

		return render_template('spell_check.html', form = form)

@app.route('/register', methods=['POST', 'GET'])
def register():
	form = RegistrationForm()

	# print (form.errors)
	# print(	session['logged_in'] )

	if request.method == 'POST':
		uname = request.form['uname']
		pword = request.form['pword']
		two_fa = request.form['two_fa']

		if len(uname) < 20 and  len(pword)<20 and len(two_fa) < 20:

			# Encrypt password and 2fa, store in dict
			pw_hash = bcrypt.generate_password_hash(pword, 12)
			two_fa_hash = bcrypt.generate_password_hash(two_fa, 12)

			newUser = User(uname, pw_hash, two_fa_hash)
			db.session.add(newUser)
			db.session.commit()


			# users_dict[uname] = [pw_hash, two_fa_hash]

			return " <a href=\"/login\" id=success >Registration Success, Please Login </a> <br> \
			 <a href = \"/register\" > Register another user </a>"

		else :
			return "<a href id=success >Registration Failure, Try again </a>"


	return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():

	form = LoginForm()
	# print(	session['logged_in'] )
	if request.method == 'POST':

		uname = request.form['uname']
		pword = request.form['pword']
		two_fa = request.form['two_fa']
	
		# Validate username, password and 2fa
		user = User.query.filter_by(username=uname).first()
		# user = users_dict[uname]
		# if uname in users_dict.keys():
		
		if user is not None:
			# pw_hash = users_dict[uname][0]
			pw_hash = user.pswd_hash

			# two_fa_hash = users_dict[uname][1]
			two_fa_hash = user.two_fa_hash			
			if bcrypt.check_password_hash(pw_hash, pword) and bcrypt.check_password_hash(two_fa_hash, two_fa) :
			
				session['username'] = uname
				return " <a href=\"/spell_check\" id=result >Login Success </a>"

			else:
				return " <a href=\"/login\" id=result >Login Failure </a>"
		else:
				return " <a href=\"/login\" id=result >Login Failure </a>"
		
	return render_template('login.html', form=form)


@app.route("/logout")
def logout():
	# session['logged_in'] = False
	session.pop('username', None)

	return home()

if __name__ == "__main__":

	# app.config['SECRET_KEY'] = "someRandomSecretKeyHahahaha"
	# db.create_all()
	# print("Successfully created DB")
	app.run(debug=True, host='127.0.0.1', port=5000)