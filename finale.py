import sqlite3
from flask import Flask, render_template, request, redirect, session, url_for, g, flash, escape



DATABASE = 'blog.db'
DEBUG = True
SECRET_KEY = "key"
USERNAME = "admin"
PASSWORD = "password"

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    if 'username' in session:
        return render_template('blog.html')
    else:
        return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != USERNAME:
            error = 'The system does not recognize that username.'
            return render_template('login.html', error=error)
        elif request.form['password'] != PASSWORD:
            error = 'The password is incorrect; please try again.'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            return redirect('/page')


@app.route('/page', methods = ['GET'])
def page():
    curs = g.db.execute('select blognum, title, date, author, content from blogs ORDER BY blognum DESC')
    blogs = [dict(blognum = row[0], title = row[1], date = row[2], author = row[3], content = row[4])
                    for row in curs.fetchall()]
    return render_template("web.html", blogs=blogs)

@app.route('/blog/add', methods = ['POST', 'GET'])
def addblog():
    title = request.form['title']
    date = request.form['date']
    author = request.form['author']
    content = request.form['content']
    g.db.execute('insert into blogs (title, date, author, content) values (?, ?, ?, ?)',
                     [request.form['title'], request.form['date'], request.form['author'], request.form['content']])
    g.db.commit()
    return redirect(url_for('page'))

@app.route('/edit/post', methods=['GET', 'POST'])
def editpost():
    if request.method == 'POST':
        g.db.execute('update blogs SET title=?, author=?, date=?, content=? WHERE blognum=?',
                     [request.form['title'], request.form['author'],request.form['date'],request.form['content'],request.form['blognum']])
        g.db.commit()
        return redirect(url_for('page'))
    return render_template('editpost.html')

@app.route('/delete/post', methods=['GET', 'POST'])
def deletepost():
    if request.method == 'POST':
        g.db.execute('DELETE FROM blogs WHERE blognum=?',
                     [request.form['blognum']])
        g.db.commit()
        return redirect(url_for('page'))
    return render_template('deletepost.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', True)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()