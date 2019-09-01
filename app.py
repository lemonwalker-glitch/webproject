from flask import Flask, render_template, Response, request, url_for, redirect, stream_with_context
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

#def gen(camera):
def gen():
    print("[INFO] starting video stream...")
    #vs = VideoStream(src=0).start()
    vs = cv2.VideoCapture(0)
    # vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)
    initial = ""
    i = 0
    recognising = True
    while recognising:
        grabbed, frame2 = vs.read()
        frame, name = recogniser.recog(frame2)
        print(name)
        if name == initial and name != None:
              i = i+1
              print(i)
              if i == 5:
                    print('reached 10')
                    vs.release()
                    cv2.destroyAllWindows()
                    print('camera is dead')
                    sse_event = 'last-item'
                    sse_data = url_for('welcome')
                    sse_id = 1
                    yield "id:{_id}\nevent:{event}\ndata:{data}\n\n".format(_id=sse_id, event=sse_event, data=sse_data)
                    recognising = False
              else:
                    initial = name
        else:
              i = 0
              initial = name
        #print(name,time)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
       
        print('hello world')
    print('everything is dead')
    #yield "id:{_id}\nevent:{event}\ndata:{data}\n\n".format(_id=sse_id, event=sse_event, data=sse_data)
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
        print(request)
        print(request.form["checkout_button"])
        #return redirect(url_for('recog'))
        return render_template('recog.html')
      elif "checkin_button" in request.form:
        print('checkin button')
        return redirect(url_for('recog'))
      else:
          return render_template('index.html')

@app.route('/recog', methods = ['GET', 'POST'])
def recog():
    """Video Streaming Home Page."""

    return render_template('recog.html')
       
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute fo an img tag."""
    print('before response function')
    return Response(stream_with_context(gen()),#gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def redirect_url():
      return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
      return render_template('welcome.html')


@app.route('/excel')
def excel():
    with open('csv_files/mycsv.csv', 'a') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Johnson', datetime.date.today().strftime('%d/%m/%Y'), datetime.datetime.now().time().strftime('%H:%M:%S')])
    return 'Welcome Johnson'    

#add logic that will route back to the index to start process again
#create another webpage displaying the log fle for someone to see
#make a cronjob in the pi that will ftp the file at the end of the day to the google drive


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=7000, threaded=True)
    

