# -*- coding: utf-8 -*-
# app.py
# Name    : 2016 Startup Weekend 병원정보시스템
# Author  : 홍승환
# Comment : 사)앱센터에서 진행하는 2016 Startup Weekend에서 대부분 국민대 팀이 만든 병원정보시스템의 Back-end API입니다.

from flask import Flask, request, jsonify
app = Flask(__name__)

# Exception Region Start

@app.errorhandler(404)
def error_not_found(error):
    return "404"

@app.errorhandler(403)
def error_access_denied(error):
    return "403"

@app.errorhandler(405)
def error_bad_request(error):
    return "405"

@app.errorhandler(500)
def error_internal_error(error):
    return "500"

# Exception Region End

# Front API Region Start

@app.route('/api', methods=['GET'])
def api():

	version = api_backend()
	return jsonify(version=version)

@app.route('/api/login', methods=['POST'])
def api_login():
	phone = request.form['phone']
	password = request.form['password']

	result, token = api_login_backend(phone, password)
	return jsonify(result=result, token=token)

@app.route('/api/logout', methods=['POST'])
def api_logout():
	token = request.form['token']

	result = api_logout_backend(token)
	return jsonify(result=result)

@app.route('/api/signup', methods=['POST'])
def api_signup():
	phone = request.form['phone']
	age = request.form['age']
	password = request.form['password']
	gender = request.form['gender']
	name = request.form['name']

	result = api_signup_backend(phone, age, password, gender, name)
	return jsonify(result=result)

# Front API Region End

# Back API Region Start

def api_backend():
	# TODO : make api_backend function
	return version

def api_login_backend(phone, password):
	# TODO : make api_login_backend function
	return result, token

def api_logout_backend(token):
	# TODO : make api_logout_backend function
	return result

def api_signup_backend(phone, age, password, gender, name):
	# TODO : make api_signup_backend function
	return result

# Back API Region End

if __name__ == '__main__':
	app.run(debug=True)
