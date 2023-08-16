from flask import (Flask, flash, make_response, redirect, render_template,
                   request, session, url_for)

from app import *

@app.route('/')
def home():
    return render_template('index.html')