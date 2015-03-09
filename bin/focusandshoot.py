import sqlite3
import RPi.GPIO as GPIO
import os, sys, time

conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), '../db/timelapsecontroller.db'))
conn.row_factory = sqlite3.Row

sleep=2

def set_pid(pid=None):
  c = conn.cursor()
  try: 
    # Update the DB counter
    c.execute("UPDATE timelapseconfig SET pid=?", ( int(pid), ) )
  except sqlite3.Error as e:
    print "An error occurred:", e.args[0]
  # Save (commit) the changes
  conn.commit()
  print "Set the PID to be ", pid

def wakeup():

  #Using Port 6 as Ground
  #Port 7 is Live

  #Sets up GPIO Pin 7 to Output
  GPIO.setup(7, GPIO.OUT)

  #Turns on GPIO Pin 7 - Enables Power to Pin 7 for focus / wake up.
  GPIO.output(7, True)
  time.sleep(2)
  GPIO.output(7, False)

def running():
  c = conn.cursor()
  try: 
    c.execute('SELECT * FROM timelapseconfig')
    config = c.fetchone()
    if config['running'] and config['count'] < config['target']:
      print "Running ({} of {})".format(config['count'], config['target'])
      return True
  except sqlite3.Error as e:
    print "An error occurred:", e.args[0]
  return False 

def getsleep():
  c = conn.cursor()
  try: 
    c.execute('SELECT * FROM timelapseconfig')
    config = c.fetchone()
    return config['sleep']
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
    c.execute("UPDATE timelapseconfig set count=count+1")
  except sqlite3.Error as e:
    print "An error occurred:", e.args[0]
  # Save (commit) the changes
  conn.commit()
  print "Incrementing counter"

if __name__ == "__main__":

  #Set the Board Mode
  GPIO.setmode(GPIO.BOARD)

  #Write (set) PID to config
  set_pid(os.getpid())

  while True:
    if ( running() ):
      wakeup()
      shoot()
      updatecounter()

    #Pause for configured # of seconds (default 2)
    sleep = getsleep()
    print "Sleeping for %r seconds.." % sleep
    time.sleep(sleep)

  #Write (unset) PID to config
  set_pid(None)

  # close the DB conn
  conn.close()

  #Stops the script and End of script clean up of the GPIO Port
  GPIO.cleanup()

