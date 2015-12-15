from flask import Flask
from flask import request
from flask import render_template
from flask import send_file
import animated_gif_function
import glob
import os
import re

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def my_form():
	gif_files = []
	gifs = []
	for file in glob.glob('/home/phantor/gifmaker.phantor.net/gifmaker2/static/gifs/*.gif'):
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
			for file in glob.glob('/home/phantor/gifmaker.phantor.net/gifmaker2/static/gifs/*.gif'):
				gif_files.append(file)
			gif_files.sort(key=os.path.getmtime)
			for file in gif_files:
				gifs.append(os.path.basename(file))
			return render_template('gif-return.html', gif_path=title, previous_gifs=gifs[-5:])
	else:
		return title[1]

if __name__ == '__main__':
	app.debug = True
	app.run()