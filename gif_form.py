from flask import Flask
from flask import request
from flask import render_template
from flask import send_file
import animated_gif_function
import glob
import os

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def my_form():
	gif_files = []
	for file in glob.glob('./static/gifs/*.gif'):
		gif_files.append(file)
	gif_files.sort(key=os.path.getmtime)
	return render_template("gif.html", previous_gifs=gif_files[-3:])

@app.route('/', methods=['POST'])
def my_form_post():
	uuid = request.form['text']
	size = request.form['size']
	title = animated_gif_function.create_gif(uuid, size)
	if title[0] != False:
		#return send_file('../public/gifs/'+title+'.gif', mimetype='image/gif')
		gif_files = []
		for file in glob.glob('./static/gifs/*.gif'):
			gif_files.append(file)
		gif_files.sort(key=os.path.getmtime)

		print gif_files[-2:]
		return render_template('gif-return.html', gif_path=title, previous_gifs=gif_files[-3:])
	else:
		return title[1]

if __name__ == '__main__':
	app.debug = True
	app.run()