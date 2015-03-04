import sys
import sqlite3
import RPi.GPIO as GPIO
import time
import math
import os

conn = sqlite3.connect(os.path.join(app.root_path, 'db/timelapsecontroller.db'))
conn.row_factory = sqlite3.Row

sleep=2

def wakeup():

  #Using Port 6 as Ground
  #Port 7 is Live

  #Sets up GPIO Pin 7 to Output
  GPIO.setup(7, GPIO.OUT)

  #Turns on GPIO Pin 7 - Enables Power to Pin 7 for focus / wake up.
  GPIO.output(7, True)

  time.sleep(2)

def running():
  c = conn.cursor()
  try: 
    c.execute('SELECT * FROM timelapseconfig')
    row = c.fetchone()
    if abs(row['running']) == 1 and math.floor(row['count']) < math.floor(row['target']):
      print "Running ({} of {})".format(abs(row['count']), abs(row['target']))
      return True
  except sqlite3.Error as e:
    print "An error occurred:", e.args[0]
  return False 

def getsleep():
  c = conn.cursor()
  try: 
    c.execute('SELECT * FROM timelapseconfig')
    row = c.fetchone()
    return abs(row['sleep'])
  except sqlite3.Error as e:
    print "An error occurred:", e.args[0]

def shoot():

  #Sets up GPIO Pin 11 to Output
  GPIO.setup(11, GPIO.OUT)

  #Pause for 2 Seconds (Hold Fire for 2 Seconds)
  #Turns on GPIO Pin 11 - Enables Power to Pin 11 to Shoot
  GPIO.output(11, True)
  time.sleep(2)
  GPIO.output(11, False)

def updatecounter():
  c = conn.cursor()
  try: 
    # Update the DB counter
    c.execute("UPDATE timelapseconfig set count=count+1.0")
  except sqlite3.Error as e:
    print "An error occurred:", e.args[0]
  # Save (commit) the changes
  conn.commit()
  print "Incrementing counter"

if __name__ == "__main__":

  #Set the Board Mode
  GPIO.setmode(GPIO.BOARD)

  while True:
    if ( running() ):
      wakeup()
      shoot()
      updatecounter()

    #Pause for configured # of seconds (default 2)
    sleep = getsleep()
    print "Sleeping for %r seconds.." % sleep
    time.sleep(sleep)

  # close the DB conn
  conn.close()

  #Stops the script and End of script clean up of the GPIO Port
  GPIO.cleanup()

