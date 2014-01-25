import os
from flask import *
import json
from werkzeug import secure_filename
from snapchat import Snapchat

GET_UPLOAD_FOLDER = './getting_uploads'
SEND_UPLOAD_FOLDER = './sending_uploads'

#create app
app = Flask(__name__)
app.config.from_object(__name__)

EXTENSIONS = ['jpeg', 'jpg', 'mp4']
IMG_EXTENSIONS = ['jpeg', 'jpg']
VID_EXTENSION = ['mp4']

@app.route("/")
def begin():
	return "don't be lazy man!"

#send image or video
#json reqs: {'username', 'password', 'file', 'recipient'}
@app.route("/send/<filetype>", methods=['GET', 'POST'])
def send(filetype):
	#login 
	data = request.get_json()
	s = Snapchat()
	s.login(data['username'],data['password'])

	"""
	#check that file has a correct ext
	filename, ext = name.split('.')
	if (filetype == "image") and (ext not in IMG_EXTENSIONS):
		print("invalid image format")
		continue
	if (filetype == "video") and (ext not in VID_EXTENSIONS):
		print("invalid video format")
		continue
	"""

	#save file on server
	snap = request.files['file']
	filename = secure_filename(snap.filename)
	snap.save(os.path.join(app.config['SEND_UPLOAD_FOLDER'], filename))
	
	#upload file to snapchat
	if (filetype == "image"):
		snapformat = "Snapchat.MEDIA_IMAGE"
	if (filetype == "video"):
		snapformat = "Snapchat.MEDIA_VIDEO"
	media_id = s.upload(snapformat, send_from_directory(app.config['SEND_UPLOAD_FOLDER'],filename))
	
	#send to recipient
	s.send(media_id, data['recipient'])
	return "success!"

"""
#getall
@app.route("/getall")
def getall():
	#login
	data = request.get_json()
	s = Snapchat()
	s.login(data['username'],data['password'])
"""

#validatelogin
