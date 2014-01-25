import os
from flask import *
import json
from werkzeug import secure_filename
from snapchat import Snapchat

import sys

#create app
app = Flask(__name__)
app.config.from_object(__name__)

EXTENSIONS = ['jpeg', 'jpg', 'mp4']
IMG_EXTENSIONS = ['jpeg', 'jpg']
VID_EXTENSION = ['mp4']

@app.route("/")
def begin():
	return "don't be lazy man!"
 
#upload img/vid file for sending 
@app.route("/upload", methods=['POST'])
def upload():
	#save file on server
	file = request.files['file']
	filename = secure_filename(file.filename)
	file.save(filename)
	return filename

#send image or video
#json reqs: {'username', 'password', 'file', 'recipient'}
@app.route("/send/<filetype>", methods=['POST'])
def send(filetype):
	#login 
	data = request.get_json()
	s = Snapchat()
	s.login(data['username'],data['password'])

	#upload file to snapchat
	if (filetype == "image"):
		snapformat = Snapchat.MEDIA_IMAGE
	if (filetype == "video"):
		snapformat = Snapchat.MEDIA_VIDEO

	media_id = s.upload(snapformat, data['fileloc'])
	
	#send to recipient
	s.send(media_id, data['recipient'])
	return "success!"

#getall
@app.route("/getall")
def getall():
	#login
	data = request.get_json()
	s = Snapchat()
	s.login(data['username'],data['password'])

	#get all snaps for the user 
	snaps = s.get_snaps()

	#download all snaps 
	allsnaps = []
	for snap in snaps:
		allsnaps.append(s.get_media(snap['id']))

	return allsnaps

#validatelogin
@app.route("/login", methods=['POST'])
def login():
	#login 
	data = request.get_json()
	s = Snapchat()
	s.login(data['username'],data['password'])

	#check if logged in
	if s.logged_in == True: 
		return "true";
	else:
		return "false";
