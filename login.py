from flask import Flask, render_template_string, request, redirect, url_for, session
import sqlite3
app=Flask(__name__)
app.secret_key='kalyan@123'

def st_db():
    with sqlite3.connect('users.db') as con:
        cur=con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT UNIQUE NOT NULL,password TEXT NOT NULL)')
        con.commit()
st_db()
def check_login():
    return 'ur' in session
@app.route('/')
def home():
    if check_login():
        return redirect(url_for('dashboard'))
    return render_template_string("""
    <html>
    <head>
        <title>ABC Home</title>
        <style>
            body { background-color: black; color: white; margin: 0; font-family: Arial, sans-serif; display: flex; }
            .sidebar { width: 250px; height: 100vh; background-color: #222; padding: 20px; position: fixed; left: 0; top: 0; }
            .sidebar h2 { text-align: center; color: #00FF00; }
            .sidebar a { display: block; color: white; text-decoration: none; padding: 10px; margin: 10px 0; border-radius: 5px; }
            .sidebar a:hover { background-color: #444; }
            .topbar { width: 100%; height: 60px; background-color: #333; position: fixed; top: 0; left: 250px; display: flex; align-items: center; padding: 0 20px; justify-content: space-between; }
            .topbar .title { font-size: 20px; color: white; }
            .topbar .menu a { margin-left: 20px; color: white; text-decoration: none; }
            .topbar .menu a:hover { text-decoration: underline; }
            .content { margin-left: 250px; margin-top: 80px; padding: 20px; text-align: center; width: 100%; }
            .logout { color: red; font-weight: bold; }
        </style>
    </head>
    <body>
        <!-- Sidebar -->
        <div class="sidebar">
            <h2>ABC Home</h2>
            <a href="/login"> Calendar</a>
            <a href="/login"> Diary Journal</a>
            <a href="/login"> Notes</a>
            <a href="/login"> Schedule</a>
            <a href="/login"> Reminders</a>
            <a href="/login"> Future Feature</a>
        </div>

        <!-- Top Bar -->
        <div class="topbar">
            <div class="title">Welcome, to ABC Home</div>
            <div class="menu">
                <a href="/login"> Goals</a>
                <a href="/login"> Tasks</a>
                <a href="/login"> Personal Database</a>
                <a href="/login" class="login"> LogIn</a>
            </div>
        </div>

        <!-- Home Content -->
        <div class="content">
            <h1>Welcome to ABC Home</h1>
            <p>Your personal productivity hub.</p>
        </div>
    </body>
    </html>
    """)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password= request.form['password']
        remember='remember' in request.form
        with sqlite3.connect('users.db') as con:
            cur=con.cursor()
            cur.execute('SELECT * FROM users WHERE email=? AND password=?',(email,password))
            ur=cur.fetchone()
        if ur :
            session['ur']=email
            if remember :
                session.permanent=True
            return redirect(url_for('dashboard'))
        else :
            return 'invalied credentials <a href="/">Try Again</a>'
    return """
            <html>
            <head>
                <title>ABC Login</title>
                <style>
                    body { background-color: black; color: white; text-align: center; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                    .container { width: 100%; max-width: 400px; padding: 20px; border-radius: 10px; }
                    input { width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; border: none; }
                    input[type="submit"] { background-color: #007BFF; color: white; cursor: pointer; }
                    a { color: #00FF00; text-decoration: none; display: block; margin-top: 10px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>ABC Login</h2>
                    <form method="POST">
                        <input type="email" name="email" placeholder="Email" required><br>
                        <input type="password" name="password" placeholder="Password" required><br>
                        <input type="checkbox" name="remember"> Remember Me<br>
                        <input type="submit" value="Log In">
                    </form>
                    <a href='/signup'>Sign Up</a>
                </div>
            </body>
            </html> """
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email= request.form['email']
        password= request.form['password']
        with sqlite3.connect('users.db') as con:
            cur=con.cursor()
            try:
                cur.execute('INSERT INTO users (email,password) VALUES (?,?)',(email,password))
                con.commit()
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                return 'Email Already Exists <a href="/signup">Try again</a>'
    return """  
        <html>
        <head>
            <title>ABC Signup</title>
            <style>
                body { background-color: black; color: white; text-align: center; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .container { width: 100%; max-width: 400px; padding: 20px; border-radius: 10px; }
                input { width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; border: none; }
                input[type="submit"] { background-color: #28A745; color: white; cursor: pointer; }
                a { color: #00FF00; text-decoration: none; display: block; margin-top: 10px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>ABC Signup</h2>
                <form method='post'>
                    <input type='email' name='email' placeholder="Email" required><br>
                    <input type='password' name='password' placeholder="Password" required><br>
                    <input type='submit' value='Sign Up'>
                </form>
                <a href='/'>Back to Login</a>
            </div>
        </body>
        </html>
            """
def render_dashboard(content=''):
    if 'ur' not in session:
        return redirect(url_for('home'))
    return f"""
    <html>
    <head>
        <title>ABC Main</title>
        <style>
            body {{ background-color: black; color: white; margin: 0; font-family: Arial, sans-serif; display: flex; }}
            .sidebar {{ width: 250px; height: 100vh; background-color: #001f3f; padding: 20px; position: fixed; left: 0; top: 0; }}
            .sidebar h2 {{ text-align: center; color: cyan; }}
            .sidebar a {{ display: block; color: white; text-decoration: none; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            .sidebar a:hover {{ background-color: #0074D9; }}
            .topbar {{width: calc(100% - 250px); height: 60px; background-color: #003366;  position: fixed; top: 0;  left: 250px;display: flex;align-items: center; padding: 0 20px;  justify-content: space-between; z-index: 1000;}}
            .logo-container {{ display: flex; align-items: center; }}
            .logo {{ width: 40px; height: 40px; border-radius: 50%; margin-right: 10px; }}
            .company-name {{ font-size: 22px; font-weight: bold; color: cyan; }}
            .menu {{ display: flex; align-items: center; }}
            .menu a {{ margin-left: 20px; color: white; text-decoration: none; }}
            .menu a:hover {{ text-decoration: underline; }}
            .user-profile {{ display: flex; align-items: center; margin-left: 20px; }}
            .avatar {{ width: 40px; height: 40px; border-radius: 50%; margin-right: 10px; border: 2px solid cyan; }}
            .username {{ font-weight: bold; color: cyan; }}
            .content {{ margin-left: 250px; margin-top: 80px; padding: 20px; text-align: center; width: 100%; }}
            .logout {{ color: red;font-weight: bold;text-decoration: none;padding: 10px 15px;border-radius: 5px;background-color: #003366 ;border: 2px solid red;}}
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h2>ABC  Company</h2> {content} 
            <a href="/Calendar">📅 Calendar</a>
            <a href="/DiaryJournal">📖 Diary Journal</a>
            <a href="/Notes">📝 Notes</a>
            <a href="/Schedule">📆 Schedule</a>
            <a href="/reminders">🔔 Reminders</a>
            <a href="/FutureFeature"># Future Feature</a>
        </div>
        <div class="topbar">
            <div class="logo-container">
                <img src="globe.svg" class="logo"> 
                <span class="company-name">ABC</span>
            </div>
            <div class="menu">
                <a href="/Goals">🎯 Goals</a>
                <a href="/Tasks">✅ Tasks</a>
                <a href="/PersonalDatabase">📂 Personal Database</a>
                <div class="user-profile">
                    <img src="pixelcut-export (7).png" class="avatar"> 
                    <span class="username">{session.get('ur', 'Guest')}</span>
                </div>
                <a href="/logout" class="logout">🚪 Logout</a>
            </div>
        </div>
        <div class="content"> 
            <h1>Welcome to ABC </h1>{content} 
            <p>Your personal productivity hub.</p>
        </div>
    </body>
    </html>
    """
@app.route('/dashboard')
def dashboard():
    if 'ur' in session:
        user_content = f"<p>Welcome, {session['ur']}!</p>"
        return render_dashboard(user_content)
    else:
        return redirect(url_for('login'))
@app.route('/Calendar')
def Calendar():
    return render_dashboard("<h1>Calendar Page</h1>")
@app.route('/DiaryJournal')
def DiaryJournal():
    return render_dashboard("<h1>Diary Journal Page</h1>")
@app.route('/Notes')
def Notes():
    return render_dashboard("<h1>Notes Page</h1>")
@app.route('/Schedule')
def Schedule():
    return render_dashboard("<h1>Schedule Page</h1>")
@app.route('/reminders')
def reminders():
    return render_dashboard("<h1>Reminders Page</h1>")
@app.route('/FutureFeature')
def FutureFeature():
    return render_dashboard("<h1>Future Feature Page</h1>")
@app.route('/Goals')
def Goals():
    return render_dashboard("<h1>Goals Page</h1>")
@app.route('/Tasks')
def Tasks():
    return render_dashboard("<h1>Tasks Page</h1>")
@app.route('/PersonalDatabase')
def PersonalDatabase():
    return render_dashboard("<h1>Personal Database Page</h1>")
@app.route('/logout')
def logout():
    session.pop('ur', None)
    return redirect(url_for('login'))
if __name__=='__main__':
    app.run(debug=True)
