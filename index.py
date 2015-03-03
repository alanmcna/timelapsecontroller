from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

import sqlite3
import math

_db = '/home/timelapsecontroller/db/timelapsecontroller.db'

@app.route('/')
@app.route('/Home', methods=['GET'])
def index(page="Home"):
    conn = sqlite3.connect(_db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    try:
        c.execute('SELECT * FROM timelapseconfig')
        row = c.fetchone()
    except sqlite3.Error as e:
        print "An error occurred:", e.args[0]
        app.logger.error("Home read - an error occurred:", e.args[0])
    running = abs(row['running'])
    count = math.floor(row['count'])
    target = math.floor(row['target'])

    conn.close()
    return render_template('index.html', page=page, running=running, count=count, target=target)

@app.route('/Start')
def start(page="Home"):
    conn = sqlite3.connect(_db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("UPDATE timelapseconfig SET running=1")
    conn.commit()
    try:
        c.execute('SELECT * FROM timelapseconfig')
        row = c.fetchone()
    except sqlite3.Error as e:
        app.logger.error("Start update - an error occurred:", e.args[0])
    running = abs(row['running'])
    count = math.floor(row['count'])
    target = math.floor(row['target'])

    conn.close()
    return render_template('index.html', page=page, running=running, count=count, target=target)

@app.route('/Stop')
def stop(page="Home"):
    conn = sqlite3.connect(_db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    try:
        c.execute("UPDATE timelapseconfig SET running=0, count=0")
        conn.commit()
    except sqlite3.Error as e:
        app.logger.error("Stop update - an error occurred:", e.args[0])

    conn.close()
    return render_template('index.html', page=page, running=False)

@app.route('/Pause')
def pause(page="Home"):
    conn = sqlite3.connect(_db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    try:
        c.execute("UPDATE timelapseconfig SET running=0")
        conn.commit()
    except sqlite3.Error as e:
        app.logger.error("Pause update - an error occurred:", e.args[0])

    conn.close()
    return render_template('index.html', page=page, running=False)


@app.route('/Count')
def count():
    conn = sqlite3.connect(_db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    try:
        c.execute("select count from timelapseconfig")
        row = c.fetchone()
        count = math.floor(row['count'])
    except sqlite3.Error as e:
        app.logger.error("Count read - an error occurred:", e.args[0])

    conn.close()
    return render_template('count.api', count=count)

@app.route('/Configuration', methods=['GET', 'POST'])
def config(page="Configuration"):
    conn = sqlite3.connect(_db, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    try:
        c.execute('SELECT * FROM timelapseconfig')
        row = c.fetchone()
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
            c.execute('UPDATE timelapseconfig SET sleep=?, target=?', (sleep, target) )
            conn.commit();
            return redirect(url_for('index'))
        except sqlite3.Error as e:
            app.logger.error("Configuration update - an error occurred:", e.args[0])

    conn.close()
    return render_template('config.html', page=page, running=running, count=count, target=target, sleep=sleep)

@app.route('/About')
def about(page="About"):
    return render_template('about.html', page=page)

if __name__ == "__main__":
    #app.debug = True
    app.run("0.0.0.0")
