
import os
from flask import Flask
from flask import request, render_template, current_app

app = Flask(__name__)
app.config.from_pyfile(os.path.join(os.pardir, 'config.py'))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    print(request)
    return render_template("upload.html")

@app.route('/chart/<chartId>', methods=['GET'])
def chart():

    return ""

# TODO: for later
@app.route('/history/<pageId>', methods=['GET'])
def history(pageId):
    # Keep the last 100 charts?
    return render_template('history.html', pageId=pageId)