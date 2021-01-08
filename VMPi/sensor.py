from sense_hat import SenseHat

import datetime
import subprocess
import shutil
from picamera import PiCamera

sense = SenseHat()
sense.clear()
sentFlag = False
sentTime = datetime.datetime.utcnow()
uploadTime = datetime.datetime.utcnow()
resetFlag = False
record = False

camera = PiCamera()
camera.start_preview()

sensorout = open('./sensordata/sensorout.txt', 'a')

F = [0, 0, 0]  # Black
O = [0, 100, 0]  # Green
R = [100, 0, 0]  # Red
W = [255, 165, 0] # Orange

running = [
F, F, F, F, F, F, F, F,
F, F, O, O, O, F, F, F,
F, F, O, F, F, O, F, F,
F, F, O, F, F, O, F, F,
F, F, O, O, O, F, F, F,
F, F, O, F, F, O, F, F,
F, F, O, F, F, O, F, F,
F, F, F, F, F, F, F, F
]

waiting = [
F, F, F, F, F, F, F, F,
F, F, F, F, F, F, F, F,
F, F, W, F, W, F, W, F,
F, F, W, F, W, F, W, F,
F, F, W, F, W, F, W, F,
F, F, F, W, F, W, F, F,
F, F, F, F, F, F, F, F,
F, F, F, F, F, F, F, F
]

notRunning = [
F, F, F, F, F, F, F, F,
F, R, F, F, F, F, F, F,
F, F, F, F, F, F, F, F,
F, F, F, F, F, F, F, F,
F, F, F, F, F, F, F, F,
F, F, F, F, F, F, F, F,
F, F, F, F, F, F, F, F,
F, F, F, F, F, F, F, F
]

sense.set_pixels(notRunning)


def split():
  shutil.copy('./sensordata/sensorout.txt', './gdVMPi/sensorout_'+str(datetime.datetime.now().strftime('%y%m%d%H%M%S.%f'))+'.txt')
  open('./sensordata/sensorout.txt', 'w')
  sensorout = open('./sensordata/sensorout.txt', 'a')
  
  
def upload():
  print("upload")
  subprocess.run(["./gdupload.sh"])
  
def cameraCap():
  currentTime = datetime.datetime.now().strftime("%H:%M:%S")
  fileLoc = f'./camera/image_{currentTime}.jpg'
  camera.capture(fileLoc)
  print("camera")

while True:
  for event in sense.stick.get_events():
    print("Stick {} {}".format(event.action, event.direction)+" set run"+str(record))
    if event.action == "released" and record == False:
      record = True
      sense.set_pixels(running)
      print("a")
    #elif event.action == "released" and record == True:
    #  record = False
    #  print("b")
      
      #sense.set_pixels(notRunning)
      
  while record:
    #if datetime.datetime.utcnow()- uploadTime > datetime.timedelta(minutes=5): #change to minutes=5 
        
    orientation = sense.get_orientation_radians()
    pi = round(orientation['pitch'],1)
    ro = round(orientation['roll'],1)
    ##ya = round(orientation['yaw'],1)
  
    acceleration = sense.get_accelerometer_raw()
    x = round(acceleration['x'],2)
    y = round(acceleration['y'],2)
    z = round(acceleration['z'],2)
    
    la = 52.26002133249245
    lo = -7.10553980574984
    
    #exception occurs
    if ro > 0.8 or ro < -0.8 or pi > 0.8 or pi < -0.8:
      print (str(ro)+" "+str(pi))
      #if an exception has been sent in the past half hour dont reset flag to allow resend
      if datetime.datetime.utcnow()-sentTime > datetime.timedelta(minutes=30): #change to minutes=30
        sentFlag = False
      
      #if an exception has not been sent recently run exception script and update flags
      if sentFlag == False:
        subprocess.run(["python3", "./bikeCrashException.py"])
        #os.system("bikeCrashException.py > exception.txt")
        print("-send exception alert-")
        sentTime = datetime.datetime.utcnow()
        sense.set_pixels(waiting)
        split()
        cameraCap()
        upload()
        sense.set_pixels(running)
        sentFlag = True
        
      #
      elif datetime.datetime.utcnow()-sentTime > datetime.timedelta(seconds=5): #change to minutes=1
        print("send exception data")
        sentTime = datetime.datetime.utcnow()
    ##print("x:", x, " y:", y, " z:", z, "pitch:", pi, " roll:", ro, " yaw:", ya)
      #print(str(datetime.datetime.now().strftime('%y%m%d %H%M%S.%f')), x, y, z, pi, ro, la, lo, "exception")
      sensorout.write((str(datetime.datetime.now().strftime('%y%m%d%H%M%S.%f')) +" "+ str(x) +" "+ str(y) +" "+ str(z) +" "+ str(pi) +" "+ str(ro) +" "+ str(la) +" "+ str(lo) +" exception\n"))
    print("-write to log-")
    sensorout.write((str(datetime.datetime.now().strftime('%y%m%d%H%M%S.%f')) +" "+ str(x) +" "+ str(y) +" "+ str(z) +" "+ str(pi) +" "+ str(ro) +" "+ str(la) +" "+ str(lo) +" record\n"))
    
    for event in sense.stick.get_events():
      print("Stick {} {}".format(event.action, event.direction)+" set not" +str(record))
      if event.action == "released" and record == True:
        record = False
        sense.set_pixels(waiting)
        split()
        cameraCap()
        upload()
        sense.set_pixels(notRunning)
        
        print("c")
    