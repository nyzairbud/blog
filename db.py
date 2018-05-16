import sqlite3 as lite
import sys

con = None

try:
    con = lite.connect('blog.db')

    c = con.cursor()

    c.execute("DROP TABLE IF EXISTS blogs;")
    c.execute("CREATE TABLE IF NOT EXISTS blogs(blog_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "title text not null,author text not null, date text not null, content text not null);")

    con.commit()


except lite.Error, e:

    if con:
        con.rollback()

    print "Error %s:" % e.args[0]
    sys.exit(1)

finally:

    if con:
        con.close()