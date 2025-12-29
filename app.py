from flask import Flask, render_template, request, redirect, url_for, session, flash
import auth
import db
import identity_disc
import dangerscan
from tron_fx import mcp_reaction
import os

app = Flask(__name__)
app.secret_key = "grid_master_key_99" # Güvenlik için bunu değiştirebilirsin

# Uygulama başladığında veritabanını hazırla (Yeni yöntem)
with app.app_context():
    db.init_db()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # auth.py içindeki login_user fonksiyonunu çağırıyoruz
    user, msg = auth.login_user(username, password)
    
    if user:
        session['username'] = user['username']
        session['role'] = user['role']
        # Giriş başarılı olunca identity_disc'i güncelle
        identity_disc.on_login(user['username'], user['role'])
        return redirect(url_for('dashboard'))
    
    flash(msg, "danger")
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    # Kullanıcının disk bilgilerini çek
    disc = identity_disc.get_disc(session['username'])
    return render_template('dashboard.html', disc=disc)

@app.route('/execute', methods=['POST'])
def execute():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    cmd = request.form.get('command', '').strip()
    if not cmd:
        return redirect(url_for('dashboard'))

    # 1. Güvenlik Taraması (dangerscan.py)
    analysis = dangerscan.analyze_text(cmd)
    
    # 2. Tehdit varsa puanı artır
    if analysis['threat_delta'] > 0:
        identity_disc.add_threat(session['username'], analysis['threat_delta'])
    
    # 3. Komutu veritabanına logla ve sayacı artır
    db.log_command(session['username'], cmd)
    identity_disc.record_command(session['username'])
    
    # 4. MCP Tepkisini al (tron_fx.py)
    disc = identity_disc.get_disc(session['username'])
    mcp_msg = mcp_reaction(disc['threat_score'], len(analysis['flagged_sentences']) > 0)
    
    flash(f"User@{session['username']}: {cmd}", "info")
    if mcp_msg:
        flash(mcp_msg, "mcp")
        
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Debug modu hataları görmeni sağlar
    app.run(host='0.0.0.0', port=5000, debug=True)