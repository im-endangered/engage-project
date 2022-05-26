from PIL import Image
from io import BytesIO
import base64
import urllib.request as ur
import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pickle
from flask import Flask, render_template, Response, redirect, url_for, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

#folder to store photos received during sign up
UPLOAD_FOLDER= './users'
#folder from where faces are fetched during execution. path is same as UPLOAD_FOLDER but since that was added later, didn't want to mess it up. not the best practice. i know :p
path = "users"

#some lists to store data
images = []
classNames = []
#listing all files in path
mylist = os.listdir(path)
#loop through the files
for cl in mylist:
    #this function extracts name of the files in order to display them if login is success
    curImg = cv2.imread(f"{path}/{cl}")
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

l = os.listdir(path)
known_face_names = [x.split(".")[0] for x in l]

#this function encodes images so that face_recognition module can work properly.
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
    return encodeList

#getting the encoded images
encoded_face_train = findEncodings(images)

#route for register page
@app.route('/register')
def register():
    return render_template('signup.html')

#route to receive the photo and username from front-end form and rename file as <username>.jpg and store it to path
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      name=request.form.get('username')+'.jpg'
      if not f or not name:
          return "Something wnet wrong"
      f.save(os.path.join(UPLOAD_FOLDER,secure_filename(name)))
      return 'Sign up successful'
  
#the homepage		
@app.route("/")
def default():
    return render_template("index.html")

#route to sign in
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        #using try catch to find any errors caused due to no face detected in webcam image
        try:
            #decode the base64 file received to normal image and load it
            decoded = ur.urlopen(request.form["file"])
            image_loaded = face_recognition.load_image_file(decoded)
            #encode the loaded image to compare with known faces
            loaded_image = face_recognition.face_encodings(image_loaded)[0]
            #check for matches
            matches = face_recognition.compare_faces(encoded_face_train, loaded_image)
            name = ""
            #check if there is similar faces
            face_distances = face_recognition.face_distance(
                encoded_face_train, loaded_image
            )
            #find the best match
            best_match_index = np.argmin(face_distances)
            #if match found then
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                #returning json 
                return {"success": True, "name": name}
        except Exception as e:
            # if match not found then return 403 as name 
            return {"success": False, "name": "403"}
    return redirect("/")

#the destination page
@app.route("/success/<name>")
def success(name):
    return render_template("welcome.html", yourName=name)

#run the whole thing
app.run(debug=True)
