import json
import sqlite3


samplej = {"name":"bhavya", "age":"22", "nationality":"indian"}
db = sqlite3.connect("test.sqlite3")

c = db.cursor()

print c

row = [('abc2', 1234)]
#c.execute('''create table person(name text, pid number)''')
c.execute('insert into person values (?,?)', row)#('abc2', 12345)")
#c.execute('''select * from person ''')



