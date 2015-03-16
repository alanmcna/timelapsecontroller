import sqlite3
import os
from datetime import datetime, timedelta
from flask import Flask, redirect, url_for, request, render_template, g

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db/timelapsecontroller.db'),
    DEBUG=True
))

def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
            print "Reading schema schema.sql"
        db.commit()
        print "Commit"

def connect_to_database():
    print app.config['DATABASE']
    return sqlite3.connect(app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def getConfig():
    db = get_db()
    cur = db.cursor()

    config = {}
    try:
        cur.execute('SELECT * FROM timelapseconfig')
        config = cur.fetchone()
    except sqlite3.Error as e:
        print "An error occurred:", e.args[0]
        app.logger.error("getConfig read - an error occurred:", e.args[0])
    return config

def setPause():
    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("UPDATE timelapseconfig SET running=0")
        db.commit()
    except sqlite3.Error as e:
        app.logger.error("Pause update - an error occurred:", e.args[0])

def setStop():
    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("UPDATE timelapseconfig SET running=0, count=0")
        db.commit()
    except sqlite3.Error as e:
        app.logger.error("Stop update - an error occurred:", e.args[0])


def setStart():
    db = get_db()
    cur = db.cursor()

    cur.execute("UPDATE timelapseconfig SET running=1")
    db.commit()
    try:
        cur.execute('SELECT * FROM timelapseconfig')
        config = cur.fetchone()
    except sqlite3.Error as e:
        app.logger.error("Start update - an error occurred:", e.args[0])

def updateConfig(r):
    config = getConfig()
    sleep = r.form.get('sleep', config['sleep'])
    target = r.form.get('target', config['target'])

    db = get_db()
    cur = db.cursor()
    try:
        cur.execute('UPDATE timelapseconfig SET sleep=?, target=?', (sleep, target) )
        db.commit();
    except sqlite3.Error as e:
        app.logger.error("Configuration update - an error occurred:", e.args[0])

def completeOn(c):
    d = datetime.now() + timedelta(seconds=(c['target']-c['count'])*c['sleep'])
    return d.strftime("%c")

@app.route('/')
@app.route('/Home', methods=['GET'])
def index(page="Home"):
    config = getConfig()
    if config['count'] >= config['target']:
        setPause()
        config = getConfig()
    return render_template('index.html', page=page, config=config, completed=completeOn(config))

@app.route('/Start')
def start(page="Home"):
    setStart()
    config = getConfig()
    return render_template('index.html', page=page, config=config, completed=completeOn(config))

@app.route('/Stop')
def stop(page="Home"):
    setStop()
    config = getConfig()
    return render_template('index.html', page=page, config=config, completed=completeOn(config))

@app.route('/Pause')
def pause(page="Home"):
    setPause()
    config = getConfig()
    return render_template('index.html', page=page, config=config, completed=completeOn(config))

@app.route('/Count')
def count():
    config = getConfig()
    return render_template('count.api', config=config)

@app.route('/Configuration', methods=['GET', 'POST'])
def config(page="Configuration"):

    if request.method == 'POST':
        updateConfig(request)
        return redirect(url_for('index'))

    config = getConfig()
    return render_template('config.html', page=page, config=config, completed=completeOn(config)) 

@app.route('/About')
def about(page="About"):
    return render_template('about.html', page=page)

if __name__ == "__main__":
    app.run("0.0.0.0")
