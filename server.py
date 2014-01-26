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
	return "welcome to shots!"

#validatelogin
@app.route("/login", methods=['POST'])
def login():
	print "here1"
	#login 
	data = request.get_json()
	s = Snapchat()
	s.login(data['username'],data['password'])

	print "here2"

	#check if logged in
	if s.logged_in == True: 
		return "true";
	else:
		return "false";
 
#send image or video
#json reqs: {'username':'', 'password':'', 'recipient':''}
@app.route("/send/<filetype>", methods=['POST'])
def send(filetype):
	print "here1!"

	#save file on server
	file = request.files['file']
	filename = secure_filename(file.filename)
	file.save(filename)

	print "here2!"

	#login 
	data = request.get_json()
	s = Snapchat()
	s.login(data['username'],data['password'])

	print "here3!"

	#upload file to snapchat
	if (filetype == "image"):
		snapformat = Snapchat.MEDIA_IMAGE
	if (filetype == "video"):
		snapformat = Snapchat.MEDIA_VIDEO

	media_id = s.upload(snapformat, filename)
	
	#send to recipient
	s.send(media_id, data['recipient'])
	return "success!"

#getall
@app.route("/getall", methods=['GET'])
def getall():
	#login
	data = request.get_json()
	s = Snapchat()
	s.login(data['username'],data['password'])

	#get all snaps for the user 
	snaps = s.get_snaps()

	for snap in snaps:
		# Download a snap
		media = s.get_media(snap['id'])
		if (media != False):
			newFile = open(snap['id'] + ".jpeg", "wb")
		  	newFileByteArray = bytearray(media)
			newFile.write(newFileByteArray)

	return "done"
