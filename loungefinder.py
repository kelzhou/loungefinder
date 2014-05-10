# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import json
import time
from datetime import datetime
import pytz

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# from https://docs.python.org/2/library/sqlite3.html#row-objects
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    # rv.row_factory = sqlite3.Row
    rv.row_factory = dict_factory
    return rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def main():
	return render_template('main.html')

def update_helper():
    dformat = "%m/%d/%Y %H:%M"
    db = get_db()
    cur = db.execute('SELECT * FROM lounges ORDER BY floor')
    entries = cur.fetchall()

    for e in entries:
        c = db.execute('SELECT * FROM reservations WHERE id = ?', (e['id'],))
        reservations = c.fetchall()
        if len(reservations):
            unchanged = True
            for r in reservations:
                # now = datetime.now(pytz.timezone('America/New_York'))
                now = time.localtime()

                start = time.strptime(r['reserve_start'], dformat)
                # start = datetime.strptime(r['reserve_start'], dformat)
                # start.replace(tzinfo=pytz.timezone('America/New_York'))

                end = time.strptime(r['reserve_end'], dformat)
                # end = datetime.strptime(r['reserve_end'], dformat)
                # end.replace(tzinfo=pytz.timezone('America/New_York'))
                
                # if ((now.date() == start.date()) and (now.date() == end.date()) and (now.time() > start.time()) 
                #   and (now.time() < end.time())):
                if now > start and now < end:
                    if not(e['free'] == 0):
                        db.execute('UPDATE lounges SET free = ? WHERE building = ? and floor = ?',
                        (0, e["building"], e["floor"]))
                        db.commit() 
                    unchanged = False
                    return

            if (unchanged):
                db.execute('UPDATE lounges SET free = ? WHERE building = ? and floor = ?',
                        (2, e["building"], e["floor"]))
                db.commit()

    return


@app.route('/lounges')
def lounges():
    db = get_db()
    harrison = []
    harnwell = []
    rodin = []

    update_helper()

    time.sleep(1)
    cur = db.execute('SELECT * FROM lounges ORDER BY floor')
    entries = cur.fetchall()
    for e in entries:
		if e['building'] == "Harrison":
			harrison.append(e)
		elif e['building'] == "Harnwell":
			harnwell.append(e)
		elif e['building'] == "Rodin":
			rodin.append(e)
    return render_template('lounges.html', entries=entries, lounges=zip(harnwell, harrison, rodin))

    # updating based on reservations
    # for e in entries:
    #   c = db.execute('SELECT * FROM reservations WHERE id = ?', (e['id'],))
    #   reservations = c.fetchall()
    #   if len(reservations):
    #       for r in reservations:
    #           now = time.localtime()
                # now = datetime.now(pytz.timezone('America/New_York'))
                # print now

                # start = time.strptime(r['reserve_start'], dformat)
                # start = datetime.strptime(r['reserve_start'], dformat)
                # start.replace(tzinfo=pytz.timezone('America/New_York'))
                # print start.date() == now.date()
                 
                # end = time.strptime(r['reserve_end'], dformat)
                # end = datetime.strptime(r['reserve_end'], dformat)
                # end.replace(tzinfo=pytz.timezone('America/New_York'))

                # if ((now.date() == start.date()) and (now.date() == end.date()) and (now.time() > start.time()) 
                #   and (now.time() < end.time()) and not(e['free'] == 0)):
                #   db.execute('UPDATE lounges SET free = ? WHERE building = ? and floor = ?',
    #                   (0, e["building"], e["floor"]))
                #   db.commit() 
                # # figure out logic?
                # elif not (now.time() > start.time() and now.time() < end.time()) and e['free'] == 0:
                #   db.execute('UPDATE lounges SET free = ? WHERE building = ? and floor = ?',
    #                   (2, e["building"], e["floor"]))
                #   db.commit() 

@app.route('/reservations')
def reservations():
    db = get_db()
    dformat = "%m/%d/%Y %H:%M"

    cur = db.execute('SELECT * FROM reservations ORDER BY id')
    entries = cur.fetchall()
    harrison = []
    harnwell = []
    rodin = []
    for e in entries:
    	# print e
    	# print e['id']
    	c = db.execute('SELECT * FROM lounges WHERE id = ? ORDER BY reserve_start', (e['id'],))
    	l = c.fetchone()
    	d = {}
    	d["floor"] = l['floor']
    	d["start"] = e["reserve_start"]
    	d["end"] = e["reserve_end"]
    	d["id"] = e['id']
    	d["i"] = e['i']
    	if l['building'] == "Harrison":
    		harrison.append(d)
    	elif l['building'] == "Harnwell":
    		harnwell.append(d)
    	elif l['building'] == "Rodin":
    		rodin.append(d)

    return render_template('reservations.html', entries=entries, harnwell=harnwell, harrison=harrison, rodin=rodin)

@app.route('/add', methods=['POST'])
def add_entry():
    if request.form['free'] == "" or request.form['building'] == "" or request.form['floor'] == "":
    	flash('Invalid data/incomplete, please try again.')
        return redirect(url_for('lounges'))

    db = get_db()
    db.execute('UPDATE lounges SET free = ? WHERE building = ? and floor = ?',
                 (request.form['free'], request.form['building'], request.form['floor']))
    db.commit()
    flash('Lounge was updated, thanks!')
    return redirect(url_for('lounges'))

@app.route('/addreserve', methods=['POST'])
def add_reserve():
    if request.form['startdate'] == "" or request.form['enddate'] == "" or request.form['building'] == "" or request.form['floor'] == "":
        flash('Invalid/incomplete data, please try again.')
        return redirect(url_for('reservations'))

    start = request.form['startdate'] + " " + request.form['starttime']
    end = request.form['enddate'] + " " + request.form['endtime']
    db = get_db()
    c = db.execute('SELECT * FROM lounges WHERE building = ? AND floor = ?', (request.form['building'], request.form['floor']))
    l = c.fetchone()
    db.execute('INSERT into reservations (id, reserve_start, reserve_end) values (?, ?, ?)',
        [l['id'], start, end])
    db.commit()
    flash('Lounge was reserved, thanks!')
    return redirect(url_for('reservations'))

@app.route('/deletereserve', methods=['POST'])
def delete_reserve():
	db = get_db()
	db.execute('DELETE FROM reservations WHERE i = ?', (request.form['i'],))
	db.commit()
	return redirect(url_for('reservations'))


if __name__ == '__main__':
    app.run()

