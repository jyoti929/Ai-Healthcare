
from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)

app.secret_key = "secretkey"

# =========================
# DATABASE SETUP
# =========================

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# USERS TABLE

cursor.execute("""

CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT

)

""")

# REPORTS TABLE

cursor.execute("""

CREATE TABLE IF NOT EXISTS reports(

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT,
    disease TEXT,
    doctor_advice TEXT,
    health_tips TEXT,
    report_time TEXT

)

""")

conn.commit()
conn.close()

# =========================
# LOGIN PAGE
# =========================

@app.route('/')
def login():

    return render_template('login.html')

# =========================
# SIGNUP PAGE
# =========================

@app.route('/signup')
def signup():

    return render_template('signup.html')

# =========================
# CREATE ACCOUNT
# =========================

@app.route('/create_user', methods=['POST'])
def create_user():

    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(

        "INSERT INTO users(username,password) VALUES(?,?)",

        (username, password)

    )

    conn.commit()
    conn.close()

    return redirect('/')

# =========================
# LOGIN USER
# =========================

@app.route('/login_user', methods=['POST'])
def login_user():

    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM users WHERE username=? AND password=?",

        (username, password)

    )

    user = cursor.fetchone()

    conn.close()

    # LOGIN SUCCESS

    if user:

        session['user'] = username

        return redirect('/home')

    # LOGIN FAILED

    else:

        return redirect('/signup')

# =========================
# HOME PAGE
# =========================

@app.route('/home')
def home():

    if 'user' not in session:

        return redirect('/')

    return render_template('home.html')

# =========================
# DASHBOARD PAGE
# =========================

@app.route('/dashboard')
def dashboard():

    if 'user' not in session:

        return redirect('/')

    return render_template('dashboard.html')

# =========================
# DISEASE PREDICTION
# =========================

@app.route('/predict', methods=['POST'])
def predict():

    patient_name = request.form['patient_name']

    fever = request.form['fever']

    fever_type = request.form.get('fever_type', '')

    cough = request.form['cough']

    headache = request.form['headache']

    fatigue = request.form['fatigue']

    # SMART AI LOGIC

    if fever == "Yes" and fever_type == "High Fever" and cough == "Yes":

        disease = "Severe Flu"

    elif fever == "Yes" and fever_type == "Low Fever":

        disease = "Normal Viral Fever"

    elif fever == "Yes" and headache == "Yes":

        disease = "Migraine"

    elif fatigue == "Yes":

        disease = "Weakness"

    else:

        disease = "Normal Fever"

    doctor_advice = "Consult nearby doctor for proper treatment."

    tips = """

    • Drink more water

    • Eat healthy food

    • Take proper sleep

    • Do breathing exercises

    """

    report_time = datetime.now().strftime("%d %B %Y | %I:%M %p")

    # SAVE REPORT

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(

        """

        INSERT INTO reports(

            patient_name,
            disease,
            doctor_advice,
            health_tips,
            report_time

        )

        VALUES(?,?,?,?,?)

        """,

        (

            patient_name,
            disease,
            doctor_advice,
            tips,
            report_time

        )

    )

    conn.commit()
    conn.close()

    return render_template(

        'dashboard.html',

        patient_name=patient_name,
        prediction=disease,
        doctor_advice=doctor_advice,
        tips=tips,
        report_time=report_time

    )

# =========================
# REPORTS PAGE
# =========================

@app.route('/reports')
def reports():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT patient_name,

        disease,

        doctor_advice,

        health_tips,

        report_time

        FROM reports

        ORDER BY id DESC

        """

    )

    reports = cursor.fetchall()

    conn.close()

    return render_template(

        'reports.html',

        reports=reports

    )

# =========================
# HEALTH PAGE
# =========================

@app.route('/health')
def health():

    return render_template('health.html')

# =========================
# HOSPITALS PAGE
# =========================

@app.route('/hospitals')
def hospitals():

    return render_template('hospitals.html')

# =========================
# ANALYTICS PAGE
# =========================

@app.route('/analytics')
def analytics():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT disease, COUNT(*)

        FROM reports

        GROUP BY disease

        """

    )

    data = cursor.fetchall()

    conn.close()

    diseases = []
    counts = []

    for row in data:

        diseases.append(row[0])
        counts.append(row[1])

    return render_template(

        'analytics.html',

        diseases=diseases,
        counts=counts

    )

# =========================
# SETTINGS PAGE
# =========================

@app.route('/settings')
def settings():

    return render_template('settings.html')

# =========================
# LOGOUT
# =========================

@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/')

# =========================
# RUN APP
# =========================

if __name__ == '__main__':

    app.run(debug=True)

