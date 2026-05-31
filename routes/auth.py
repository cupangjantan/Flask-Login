from flask import Blueprint, render_template, redirect, request, url_for, session
import config.config as config
import hashlib

auth = Blueprint('auth', __name__)

@auth.route('/')
def main():
    return redirect(url_for('auth.login'))

@auth.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username and not password:
            return render_template('login.html', error="Username dan Password tidak boleh kosong")
        elif not username:
            return render_template('login.html', error='Username tidak boleh kosong')
        elif not password:
            return render_template('login.html', error='Password tidak boleh kosong')
        
        password_hashed = hashlib.sha256(password.encode()).hexdigest()
        conn = config.get_conn()

        if not conn:
            return render_template('login.html', error='Koneksi database gagal')
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()

            # ✅ Cek user None dulu
            if user is None:
                return render_template('login.html', error='Username tidak ditemukan')
            
            if user and user['password'] == password_hashed:
                session['username'] = user['username']
                session['user_id'] = user['id']
                session.permanent = True
                return redirect(url_for('dashboard.home'))
            else:
                print(f"{user['password']} dan {password_hashed}")
                return render_template('login.html', error='Password anda salah')

        except Exception as e:
            print(f'Database error: {e}')
            return render_template('login.html', error='Terjadi kesalahan sistem')
        finally:
            if conn:  # ✅ Cek conn sebelum close
                conn.close()

    return render_template('login.html')      