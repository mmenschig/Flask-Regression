
# TODO: implement logging

import os
import json
from flask import Flask
from flask import request, render_template, flash, redirect, url_for, send_file, Markup
from time import time
from werkzeug.utils import secure_filename

# Custom packages
from app.utils.helpers import allowed_file
from app.statistics import linear

# Instantiating app
app = Flask(__name__)
app.config.from_pyfile(os.path.join(os.pardir, 'config.py'))

# Definitions of Routes
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # flash(message="Invalid form", category="alert-danger")
    if request.method == 'POST':
        # Parsing form data
        request_body = {}
        request_body["chart_title"] = request.form["chartTitle"] or ''

        try:
            file = request.files['inputFile']
        except KeyError:
            msg = Markup("<strong>Error:</strong> No file selected. Please provide a data file.")
            flash(msg, category='alert-danger')
            # TODO: log e to file
            return redirect(request.url)

        if file.filename == '' or not allowed_file(file.filename):
            msg = Markup("<strong>Error:</strong> Invalid file name. Please provide either .csv or .txt")
            flash(msg, category="alert-danger")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            timestamp = int(round(time() * 1000))
            filename = "{}_{}".format(timestamp,secure_filename(file.filename)) # Make this unix timestamp
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            linear.main(timestamp=timestamp, filename=filename, request_body=request_body)
            return redirect(url_for('statistics', chartId=timestamp))
    # GET Method
    return render_template("upload.html")


@app.route('/statistics/<int:chartId>', methods=['GET'])
def statistics(chartId):
    return render_template("statistics.html", chartId=chartId)


@app.route('/chart/<int:chartId>', methods=['GET'])
def chart(chartId):
    path = 'charts/{}.png'.format(chartId)
    return send_file(path, mimetype='image/png')

@app.route('/changelog')
def changelog():
    # Load Changelog.json and pass to template
    with open('app/changelog.json', 'r') as f:
        changelog=json.load(f)
        return render_template('changelog.html', changelog=changelog)

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def internal_server_error():
    return render_template("errors/500.html"), 500
