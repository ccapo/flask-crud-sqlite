from flask import Flask, render_template
from markupsafe import escape
import sqlite3
import signal
import os

app = Flask(__name__)

# Define app config parameters
app.config['HOST'] = os.getenv('HOST', '0.0.0.0')
app.config['PORT'] = os.getenv('PORT', 5050)
app.config['ENV'] = os.getenv('ENV', 'development')
app.config['DEBUG'] = os.getenv('DEBUG', False)
app.config['DATABASE'] = os.path.join(os.getcwd(), './data/db.sqlite3')

@app.template_filter('reverse')
def bool_transform(s):
    if s == 't':
        return "True"
    elif s == 'f':
        return "False"
    else:
        return f"Unknown value: {s}"
app.jinja_env.filters['bool_transform'] = bool_transform

# Our signal handler
def signal_handler(signum, frame):
  print(f"\nSignal {signum} received, exiting...")
  exit(0)

# Register our signal handler with desired signal
signal.signal(signal.SIGHUP, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGQUIT, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Connect to DB
def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# Routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/customers', methods=['GET'])
def customers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE active = 't';")
    customers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('customers.html', customers=customers)

@app.route('/lists', methods=['GET'])
def lists():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM lists;")
    lists = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('lists.html', lists=lists)

@app.route('/list/phase0', methods=['GET'])
def phase0_list():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE name = 'CompanyA' AND active = 't' AND autodeferral = 'f';")
    customers = cur.fetchall()
    cur.execute("SELECT * FROM lists WHERE name = 'Phase 0';")
    linfo = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('list.html', customers=customers, linfo=linfo)

@app.route('/list/phase1', methods=['GET'])
def phase1_list():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE platforms LIKE '%linux%' AND active = 't' AND autodeferral = 'f';")
    customers = cur.fetchall()
    cur.execute("SELECT * FROM lists WHERE name = 'Phase 1';")
    linfo = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('list.html', customers=customers, linfo=linfo)

@app.route('/list/phase2', methods=['GET'])
def phase2_list():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE vdi = 't' AND active = 't' AND autodeferral = 'f';")
    customers = cur.fetchall()
    cur.execute("SELECT * FROM lists WHERE name = 'Phase 2';")
    linfo = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('list.html', customers=customers, linfo=linfo)

@app.route('/list/phase3', methods=['GET'])
def phase3_list():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE region IN ('us001','ca001','eu001') AND active = 't' AND autodeferral = 'f';")
    customers = cur.fetchall()
    cur.execute("SELECT * FROM lists WHERE name = 'Phase 3';")
    linfo = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('list.html', customers=customers, linfo=linfo)

@app.route('/assignment', methods=['GET'])
def assignment():
    return render_template('assignment.html')

@app.route('/assignment/create/release/setup', methods=['GET','POST'])
def create_setup():
    return render_template('create_release.html')

@app.route('/assignment/update/release/setup', methods=['GET','POST'])
def update_setup():
    return render_template('update_release.html')

@app.route('/assignment/create/release/rollout', methods=['GET','POST'])
def create_rollout():
    return render_template('create_rollout.html')

@app.route('/assignment/update/release/rollout', methods=['GET','POST'])
def update_rollout():
    return render_template('update_rollout.html')

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
