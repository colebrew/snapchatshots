import os
from flask import *
import json
from werkzeug import secure_filename
from snapchat import Snapchat

import sys

#create app
app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

EXTENSIONS = ['jpeg', 'jpg', 'mp4']
IMG_EXTENSIONS = ['jpeg', 'jpg']
VID_EXTENSION = ['mp4']

@app.route("/")
def begin():
	print "Instantiating Snapchat"
	s = Snapchat()
	print "Loging in"
	s.login("poopinin", "poopinin")
	
	#send to recipient
	print "Uploading"
	media_id = s.upload(Snapchat.MEDIA_IMAGE, "./largebar.jpg")
	print "Sending to Snapchat"
	s.send(media_id, "ckushna")

	return "welcome to shots!"

#validatelogin
@app.route("/login", methods=['POST'])
def login():
	#login 
	s = Snapchat()
	s.login(request.args.get('username'), request.args.get('password'))

	#check if logged in
	if s.logged_in == True: 
		return {"success":True};
	else:
		return {"success":False};
 
#send image or video
#json reqs: {'username':'', 'password':'', 'recipient':''}
@app.route("/send/<filetype>", methods=['POST'])
def send(filetype):

	#save file on server
	file = request.files['file']
	filename = secure_filename(file.filename)
	file.save(filename)

	print "here2!"

	#login 
	s = Snapchat()
	s.login(request.args.get('username'),request.args.get('username'))

	print "here3!"

	#upload file to snapchat
	if (filetype == "image"):
		snapformat = Snapchat.MEDIA_IMAGE
	if (filetype == "video"):
		snapformat = Snapchat.MEDIA_VIDEO

	media_id = s.upload(snapformat, filename)
	
	#send to recipient
	s.send(media_id, request.args.get('recipient'))
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

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
