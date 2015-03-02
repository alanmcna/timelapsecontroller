import sqlite3
conn = sqlite3.connect('/home/timelapsecontroller/db/timelapsecontroller.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE timelapseconfig
             (sleep real, running real, target real, count real)''')

# Insert a row of data
c.execute("INSERT INTO timelapseconfig ('sleep', 'running', 'target', 'count') VALUES (2,0,100,0)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
