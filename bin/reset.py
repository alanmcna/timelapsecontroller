import sqlite3
conn = sqlite3.connect('/home/timelapsecontroller/db/timelapsecontroller.db')
c = conn.cursor()

# Create table
c.execute('''UPDATE timelapseconfig SET sleep=5.0, running=0.0, target=100.0, count=0.0''')

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
