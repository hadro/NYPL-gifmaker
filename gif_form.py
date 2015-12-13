from flask import Flask
from flask import request
from flask import render_template
from flask import send_file
import animated_gif_function

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def my_form():
        return render_template("gif.html")

@app.route('/', methods=['POST'])
def my_form_post():
	uuid = request.form['text']
	size = request.form['size']
	title = animated_gif_function.create_gif(uuid, size)
	if title[0] != False:
		#return send_file('../public/gifs/'+title+'.gif', mimetype='image/gif')
		return render_template('gif-return.html', gif_path=title)
	else:
		return title[1]

if __name__ == '__main__':
	app.debug = True
	app.run()