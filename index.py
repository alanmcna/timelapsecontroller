from flask import Flask
from flask import render_template
app = Flask(__name__)

import sqlite3
import math

@app.route('/')
@app.route('/Home')
def index(page="Home"):
    conn = sqlite3.connect('/home/timelapsecontroller/db/timelapsecontroller.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    try:
        c.execute('SELECT * FROM timelapseconfig')
        row = c.fetchone()
    except sqlite3.Error as e:
        print "An error occurred:", e.args[0]
    running = abs(row['running'])

    conn.close()
    return render_template('index.html', page=page, running=running, count=math.floor(row['count']), target=math.floor(row['target']))

@app.route('/Start')
def start(page="Home"):
    conn = sqlite3.connect('/home/timelapsecontroller/db/timelapsecontroller.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("UPDATE timelapseconfig SET running=1")
    conn.commit()
    try:
        c.execute('SELECT * FROM timelapseconfig')
        row = c.fetchone()
    except sqlite3.Error as e:
        print "An error occurred:", e.args[0]
    running = abs(row['running'])

    conn.close()
    return render_template('index.html', page=page, running=running, count=math.floor(row['count']), target=math.floor(row['target']))

@app.route('/Stop')
def stop(page="Home"):
    conn = sqlite3.connect('/home/timelapsecontroller/db/timelapsecontroller.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("UPDATE timelapseconfig SET running=0, count=0")
    conn.commit()

    conn.close()
    return render_template('index.html', page=page, running=False)

@app.route('/Pause')
def pause(page="Home"):
    conn = sqlite3.connect('/home/timelapsecontroller/db/timelapsecontroller.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("UPDATE timelapseconfig SET running=0")
    conn.commit()

    conn.close()
    return render_template('index.html', page=page, running=False)


@app.route('/Count')
def count():
    conn = sqlite3.connect('/home/timelapsecontroller/db/timelapsecontroller.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    try:
        c.execute("select count from timelapseconfig")
        row = c.fetchone()
        count = math.floor(row['count'])
    except sqlite3.Error as e:
        print "An error occurred:", e.args[0]

    conn.close()
    return render_template('count.api', count=count)

@app.route('/Configuration')
def config(page="Configuration"):
    conn = sqlite3.connect('/home/timelapsecontroller/db/timelapsecontroller.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    try:
        c.execute('SELECT * FROM timelapseconfig')
        row = c.fetchone()
    except sqlite3.Error as e:
        print "An error occurred:", e.args[0]
    running = abs(row['running'])
    count=math.floor(row['count'])
    target=math.floor(row['target'])
    sleep=math.floor(row['sleep'])

    conn.close()
    return render_template('config.html', page=page, running=running, count=count, target=target, sleep=sleep)

if __name__ == "__main__":
    app.debug = True
    app.run("0.0.0.0")
