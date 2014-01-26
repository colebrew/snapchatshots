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
	#login 
	data = request.get_json()
	s = Snapchat()
	s.login(data['username'],data['password'])

	#check if logged in
	if s.logged_in == True: 
		return "true";
	else:
		return "false";
 
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

def download(s, snap):
    """Download a specific snap, given output from s.get_snaps()."""

    id = snap['id']
    name = snap['sender']
    ts = str(snap['sent']).replace(':', '-')

    result = s.get_media(id)

    if not result:
        return False

    ext = s.is_media(result)
    filename = '{}_{}_{}.{}'.format(ts, name, id, ext)
    path = PATH + filename
    with open(path, 'wb') as fout:
        fout.write(result)
    return True
