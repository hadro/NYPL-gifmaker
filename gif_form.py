from flask import Flask
from flask import request
from flask import render_template
from flask import send_file
import animated_gif_function

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("gif.html")

@app.route('/', methods=['GET', 'POST'])
def my_form_post():
	if request.method == 'GET':	
		uuid = request.form['text']
		title = animated_gif_function.create_gif(uuid)
		return send_file('./gifs/'+title+'.gif', mimetype='image/gif')
	if request.method == 'POST':
		uuid = request.form['text']
		title = animated_gif_function.create_gif(uuid)
		return send_file('./gifs/'+title+'.gif', mimetype='image/gif')

if __name__ == '__main__':
    app.debug = True
    app.run()