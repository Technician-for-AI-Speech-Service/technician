from flask import Flask, jsonify, Blueprint, redirect, render_template, send_from_directory, session, url_for, flash
from flask_mysqldb import MySQL
import pymysql
import pandas as pd
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination, get_page_parameter
import secrets
import os

app = Flask(__name__, static_url_path='/static')
app.secret_key = secrets.token_hex(16)


# connection = pymysql.connect(host='',  port = 3307, user = ) # 아래와 동일

app.config['MYSQL_HOST'] = 'project-db-stu3.smhrd.com'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = 'Insa4_IOTB_final_3'
app.config['MYSQL_PASSWORD'] = 'aischool3'
app.config['MYSQL_DB'] = 'Insa4_IOTB_final_3'

mysql = MySQL(app)

@app.route('/')
def main():
    return render_template('/myApp/main/main.html')

@app.route('/user/login')
def loginForm():
    return render_template('/myApp/user/loginForm.html')

@app.route('/user/loginMain')
def loginMain():
    return render_template('/myApp/main/main_login.html')

@app.route('/user/signup')
def signup():
    return render_template('/myApp/user/signup.html')



# 실행
if __name__ == '__main__':
    app.run(debug=True)