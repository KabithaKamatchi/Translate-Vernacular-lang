from flask import (Flask, flash, make_response, redirect, render_template,
                   request, session, url_for)

from app import *

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/service')
def service():
    return render_template('audioin.html')