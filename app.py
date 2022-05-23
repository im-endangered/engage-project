from PIL import Image
from io import BytesIO
import base64
import urllib.request as ur
import face_recognition
import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pickle
from flask import Flask, render_template, Response, redirect, url_for, request, jsonify
from werkzeug.utils import secure_filename


app = Flask(__name__)
UPLOAD_FOLDER= './users'

path = "users"
app = Flask(__name__)
images = []
classNames = []
mylist = os.listdir(path)
for cl in mylist:
    curImg = cv2.imread(f"{path}/{cl}")
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

l = os.listdir(path)
known_face_names = [x.split(".")[0] for x in l]


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
    return encodeList


encoded_face_train = findEncodings(images)

@app.route('/register')
def register():
    return render_template('signup.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      name=request.form.get('username')+'.jpg'
      if not f or not name:
          return "Something wnet wrong"
      f.save(os.path.join(UPLOAD_FOLDER,secure_filename(name)))
      return 'Sign up successful'
		
@app.route("/")
def default():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            decoded = ur.urlopen(request.form["file"])
            image_loaded = face_recognition.load_image_file(decoded)
            loaded_image = face_recognition.face_encodings(image_loaded)[0]
            matches = face_recognition.compare_faces(encoded_face_train, loaded_image)
            name = ""
            face_distances = face_recognition.face_distance(
                encoded_face_train, loaded_image
            )
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                return {"success": True, "name": name}
        except Exception as e:
            # print(e)
            return {"success": True, "name": "403"}
    return redirect("/")


@app.route("/success/<name>")
def success(name):
    return render_template("welcome.html", yourName=name)


app.run(debug=True)
