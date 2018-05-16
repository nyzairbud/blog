import sqlite3 as lite
import sys

con = None

try:
    con = lite.connect('blog.db')

    c = con.cursor()

    c.execute("DROP TABLE IF EXISTS blogs;")
    c.execute("CREATE TABLE IF NOT EXISTS blogs(blognum INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "title text not null,author text not null, date text not null, content text not null);")
    c.execute(
        "INSERT INTO blogs(title,author,date,content) VALUES('Blog Site', 'The End', 'May 2, 2018', 'this is how it all ends!');")

    con.commit()


except lite.Error, e:

    if con:
        con.rollback()

    print "Error %s:" % e.args[0]
    sys.exit(1)

finally:

    if con:
        con.close()