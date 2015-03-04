import sqlite3
import math
import os
from flask import Flask, redirect, url_for, request, render_template, g

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db/timelapsecontroller.db'),
    DEBUG=True
))

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
            print "Reading schema schema.sql"
        db.commit()
        print "Commit"

def connect_to_database():
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

@app.route('/')
@app.route('/Home', methods=['GET'])
def index(page="Home"):
    cur = get_db().cursor()

    try:
        cur.execute('SELECT * FROM timelapseconfig')
        row = cur.fetchone()
    except sqlite3.Error as e:
        print "An error occurred:", e.args[0]
        app.logger.error("Home read - an error occurred:", e.args[0])
    running = abs(row['running'])
    count = math.floor(row['count'])
    target = math.floor(row['target'])

    return render_template('index.html', page=page, running=running, count=count, target=target)

@app.route('/Start')
def start(page="Home"):
    db = get_db()
    cur = db.cursor()

    cur.execute("UPDATE timelapseconfig SET running=1")
    db.commit()
    try:
        cur.execute('SELECT * FROM timelapseconfig')
        row = cur.fetchone()
    except sqlite3.Error as e:
        app.logger.error("Start update - an error occurred:", e.args[0])
    running = abs(row['running'])
    count = math.floor(row['count'])
    target = math.floor(row['target'])

    return render_template('index.html', page=page, running=running, count=count, target=target)

@app.route('/Stop')
def stop(page="Home"):
    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("UPDATE timelapseconfig SET running=0, count=0")
        db.commit()
    except sqlite3.Error as e:
        app.logger.error("Stop update - an error occurred:", e.args[0])

    return render_template('index.html', page=page, running=False)

@app.route('/Pause')
def pause(page="Home"):
    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("UPDATE timelapseconfig SET running=0")
        db.commit()
    except sqlite3.Error as e:
        app.logger.error("Pause update - an error occurred:", e.args[0])

    return render_template('index.html', page=page, running=False)


@app.route('/Count')
def count():
    cur = get_db().cursor()

    try:
        cur.execute("select count from timelapseconfig")
        row = cur.fetchone()
        count = math.floor(row['count'])
    except sqlite3.Error as e:
        app.logger.error("Count read - an error occurred:", e.args[0])

    return render_template('count.api', count=count)

@app.route('/Configuration', methods=['GET', 'POST'])
def config(page="Configuration"):
    db = get_db()
    cur = db.cursor()

    try:
        cur.execute('SELECT * FROM timelapseconfig')
        row = cur.fetchone()
    except sqlite3.Error as e:
        app.logger.error("Configuration read - an error occurred:", e.args[0])
    running = abs(row['running'])
    count=math.floor(row['count'])
    target=math.floor(row['target'])
    sleep=math.floor(row['sleep'])

    if request.method == 'POST':
        sleep = request.form.get('sleep', sleep)
        target = request.form.get('target', target)

        try:
            cur.execute('UPDATE timelapseconfig SET sleep=?, target=?', (sleep, target) )
            db.commit();
            return redirect(url_for('index'))
        except sqlite3.Error as e:
            app.logger.error("Configuration update - an error occurred:", e.args[0])

    return render_template('config.html', page=page, running=running, count=count, target=target, sleep=sleep)

@app.route('/About')
def about(page="About"):
    return render_template('about.html', page=page)

if __name__ == "__main__":
    app.run("0.0.0.0")
