from flask import Blueprint, render_template, redirect, request, url_for, session
import config.config as config
import hashlib

dash = Blueprint('dashboard', __name__)

@dash.route('/home/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return redirect(url_for('auth.login'))

@dash.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))