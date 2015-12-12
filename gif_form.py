from flask import Flask
from flask import request
from flask import render_template
from flask import send_file
import animated_gif_function

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("gif.html")

@app.route('/', methods=['POST'])
def my_form_post():
	uuid = request.form['text']
	title = animated_gif_function.create_gif(uuid)
	return send_file(title+'.gif', mimetype='image/gif')

if __name__ == '__main__':
    app.debug = True
    app.run()