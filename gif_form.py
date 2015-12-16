from flask import Flask, request, render_template, send_file
#from flask_s3 import FlaskS3
import boto3
import glob
import os
import re
import animated_gif_function


app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def my_form():
	gif_files = []
	gifs = []
	for file in glob.glob('static/gifs/*.gif'):
		gif_files.append(file)
	gif_files.sort(key=os.path.getmtime)
	for file in gif_files:
		gifs.append(os.path.basename(file))
	return render_template("gif.html", previous_gifs=gifs[-4:])

@app.route('/', methods=['POST'])
def my_form_post():
	url = request.form['text']
	size = request.form['size']
	
	#Check for last UUID in a URL:
	uuid = None
	for uuid in re.finditer(r'([a-f0-9-]{36})', url):
		pass
	if uuid != None:
		uuid = uuid.group()
	else:
		return "That doesn't look like a URL we can handle! Try again?"

	title = animated_gif_function.create_gif(uuid, size)
	if title[0] != False:
			gif_files = []
			gifs = []
			for file in glob.glob('static/gifs/*.gif'):
				gif_files.append(file)
			gif_files.sort(key=os.path.getmtime)
			for file in gif_files:
				gifs.append(os.path.basename(file))
			return render_template('gif-return.html', gif_path=title, previous_gifs=gifs[-5:])
	else:
		return title[1]

if __name__ == '__main__':
	#app.debug = True
	app.run()