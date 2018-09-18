
import os
import json
from flask import Flask
from flask import request, render_template, flash, redirect, url_for, send_file
from time import time
from werkzeug.utils import secure_filename
from app.utils.helpers import allowed_file

from app.statistics import linear


app = Flask(__name__)
app.config.from_pyfile(os.path.join(os.pardir, 'config.py'))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # flash(message="Invalid form", category="alert-danger")
    if request.method == 'POST':

        # Grabbing form input
        request_body = {}
        request_body["chart_title"] = request.form["chartTitle"]
        request_body["y_axis_label"] = request.form["yAxisLabel"]
        request_body["x_axis_label"] = request.form["xAxisLabel"]
        request_body["field_separator"] = request.form["fieldSeparator"]


        file = request.files['inputFile']
        # TODO: flash message if file not provided

        # TODO: fix message flashing
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            timestamp = int(round(time() * 1000))
            filename = "{}_{}".format(timestamp,secure_filename(file.filename)) # Make this unix timestamp
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # TODO: call chart creation here
            linear.main(timestamp=timestamp, filename=filename, request_body=request_body)
            return redirect(url_for('statistics', chartId=timestamp))
            # TODO: after upload, we need to generate chart, and redirect to chart-url
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
