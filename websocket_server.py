import time
import random
import json
import datetime
import os
from tornado import websocket, web, ioloop
from datetime import timedelta
from random import randint
import datetime
import sqlite3


class WebSocketHandler(websocket.WebSocketHandler):
  # Addition for Tornado as of 2017, need the following method
  # per: http://stackoverflow.com/questions/24851207/tornado-403-get-warning-when-opening-websocket/25071488#25071488
  def check_origin(self, origin):
    return True

  #on open of this socket
  def open(self):
    print ('Connection established.')
    #ioloop to wait for 3 seconds before starting to send data
    ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=3), self.send_data)

 #close connection
  def on_close(self):
    print ('Connection closed.')

  def check_origin(self, origin):
    return True

  # Our function to send new (random) data for charts
  def send_data(self):
    print ("Sending Data")
    #create a bunch of random data for various dimensions we want
    c = random.randrange(1,50)
    v = random.randrange(1,50)
    p = c*v
    time = str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) + ":" + str(datetime.datetime.now().second) + ":" + str(datetime.datetime.now().microsecond)
    db = sqlite3.connect('new1db.db')
    
    
    
    print(time)
    
    
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS energy33(id INTEGER PRIMARY KEY,time1 INTEGER , current INTEGER,
                           voltage INTEGER, power INTEGER) 
    ''')
    cursor.execute('''INSERT INTO energy33(time1 ,current,voltage,power)
                      VALUES(?,?,?,?)''', (time,c,v,p,))
    cursor.execute('''SELECT power,voltage,current,time1 FROM energy33 ORDER BY id DESC LIMIT 1;''')
    result_set = cursor.fetchall()
    db.commit()
    for x_result in result_set:
        print(x_result[0],x_result[1],x_result[2],x_result[3])
        
        
    point_data = {
        'current': x_result[1],
        'voltage' :x_result[2],
        'power': x_result[0],
        'time': x_result[3]
    }

    print (point_data)

    #write the json object to the socket
    self.write_message(json.dumps(point_data))

    #create new ioloop instance to intermittently publish data
    ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1), self.send_data)

if __name__ == "__main__":
  #create new web app w/ websocket endpoint available at /websocket
  print ("Starting websocket server program. Awaiting client requests to open websocket ...")
  application = web.Application([(r'/static/(.*)', web.StaticFileHandler, {'path': r'C:\Users\sai\high\chart1.html'}),
                                 (r'/websocket', WebSocketHandler)])
  application.listen(8002)
  ioloop.IOLoop.instance().start()
