from flask import Blueprint, render_template, redirect, request, url_for, session
import app.config.config as config
import hashlib
from app import bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/')
def main():
    return redirect(url_for('auth.login'))

@auth.route('/login/', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard.home'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username and not password:
            return render_template('login.html', error="Username dan Password tidak boleh kosong")
        elif not username:
            return render_template('login.html', error='Username tidak boleh kosong')
        elif not password:
            return render_template('login.html', error='Password tidak boleh kosong')
        
        password_hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        conn = config.get_conn()

        if not conn:
            return render_template('login.html', error='Koneksi database gagal')
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()

            if user is None:
                return render_template('login.html', error='Username tidak ditemukan')
            
            if user and  bcrypt.check_password_hash(user['password'], password):
                session['username'] = user['username']
                session['user_id'] = user['id']
                session.permanent = True
                return redirect(url_for('dashboard.home'))
            else:
                return render_template('login.html', error='Password anda salah')

        except Exception as e:
            print(f'Database error: {e}')
            return render_template('login.html', error='Terjadi kesalahan sistem. Silahkan coba lagi.')
        finally:
            if conn:  
                conn.close()

    return render_template('login.html')   

@auth.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username and not password and not confirm_password:
            return render_template('register.html', error="Username, Password, dan Konfirmasi Password tidak boleh kosong")
        elif not username:
            return render_template('register.html', error='Username tidak boleh kosong')
        elif not password:
            return render_template('register.html', error='Password tidak boleh kosong')
        elif not confirm_password:
            return render_template('register.html', error='Konfirmasi Password tidak boleh kosong')
        elif password != confirm_password:
            return render_template('register.html', error='Password dan Konfirmasi Password tidak cocok')

        password_hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        conn = config.get_conn()

        if not conn:
            return render_template('register.html', error='Koneksi database gagal')
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                return render_template('register.html', error='Username sudah digunakan')

            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password_hashed))
            conn.commit()
            cursor.close()

            return redirect(url_for('auth.login'))

        except Exception as e:
            print(f'Database error: {e}')
            return render_template('register.html', error='Terjadi kesalahan sistem. Silahkan coba lagi.')
        finally:
            if conn:  
                conn.close()

    return render_template('register.html')