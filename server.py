import os
from flask import *
import json
from werkzeug import secure_filename
from snapchat import Snapchat

GET_UPLOAD_FOLDER  = '/shotsWebServer/getting_uploads'
SEND_UPLOAD_FOLDER = '/shotsWebServer/sending_uploads'

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
	file.save(os.path.join(app.config['SEND_UPLOAD_FOLDER'], filename))
	return filename
	#return redirect(url_for('uploaded_file', filename=filename))

#send image or video
#json reqs: {'username', 'password', 'file', 'recipient'}
@app.route("/send/<filetype>", methods=['POST'])
def send(filetype):
	#login 
	return "success!"
	data = request.get_json()
	s = Snapchat()
	s.login(data['username'],data['password'])
	#upload file to snapchat
	if (filetype == "image"):
		snapformat = "Snapchat.MEDIA_IMAGE"
	if (filetype == "video"):
		snapformat = "Snapchat.MEDIA_VIDEO"
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

#validatelogin
@app.route("/login", methods=['POST', 'GET'])
def login():
	error = None
	data = request.get_json()
	if request.method == 'POST':
		s = Snapchat()
		s.login(data['username'],data['password'])
		return 'made it'
	else:
		error = 'Invalid http request'
	return error