from flask import Flask, render_template, Response, request, url_for, redirect
import cv2
import numpy as np
import os
import csv
import datetime
import pi_face_recognition as recogniser
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time


# cascade for face detection
print("[INFO] loading encodings + face detector...")
#data = pickle.loads(open(args["encodings"], "rb").read())
data = pickle.loads(open("encodings.pickle", "rb").read())
#detector = cv2.CascadeClassifier(args["cascade"])
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def index():
      if "checkout_button" in request.form: #name="checkout_button" is the value request.form['checkout_button] = checkout  (value)
        print(request.form["checkout_button"])
        return redirect(url_for('recog'))
      elif "checkin_button" in request.form:
        print('checkin button')
        return redirect(url_for('recog'))
      else:
          return render_template('index.html')

@app.route('/recog')
def recog():
    """Video Streaming Home Page."""
    return render_template('recog.html')

#def gen(camera):
def gen():
    
    print("[INFO] starting video stream...")
    #vs = VideoStream(src=0).start()
    vs = cv2.VideoCapture(0)
    # vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)
    
    while True:
        
        grabbed, frame2 = vs.read()
        frame = recogniser.recog(frame2)
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
'''
cam.release()
    Akshay  27
Akshay  28
Akshay  29
Debugging middleware caught exception in streamed response at a point where response headers were already sent.
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/werkzeug/wsgi.py", line 870, in __next__
    return self._next()
  File "/usr/lib/python3/dist-packages/werkzeug/wrappers.py", line 82, in _iter_encoded
    for item in iterable:
  File "/home/pi/webapp/app.py", line 72, in gen
    return render_template('/')
  File "/usr/lib/python3/dist-packages/flask/templating.py", line 133, in render_template
    ctx.app.update_template_context(context)
AttributeError: 'NoneType' object has no attribute 'app'
'''
    
       
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute fo an img tag."""
    return Response(gen(),#gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/welcome')
def welcome():
    with open('csv_files/mycsv.csv', 'a') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Johnson', datetime.date.today().strftime('%d/%m/%Y'), datetime.datetime.now().time().strftime('%H:%M:%S')])
    return 'Welcome Johnson'    

#add logic that will route back to the index to start process again
#create another webpage displaying the log fle for someone to see
#make a cronjob in the pi that will ftp the file at the end of the day to the google drive


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=7000, threaded=True)
    

