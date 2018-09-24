# TODO: implement logging

import os
import json
from flask import Flask
from flask import request, render_template, flash, redirect, url_for, \
                  send_file, Markup, session
from flask_mail import Mail, Message
import asyncio
from time import time
from werkzeug.utils import secure_filename

# Custom packages
from app.utils.helpers import allowed_file
from app.statistics import linear

# Instantiating app
app = Flask(__name__)
app.config.from_pyfile(os.path.join(os.pardir, 'config.py'))

mail = Mail(app)

# TODO: move to mail module
async def send_email(recipients):
    """ Sends stats information to user. """
    with app.app_context():
        msg = Message("Upload",
            sender="marian.menschig@googlemail.com",
            recipients=recipients)

    mail.send(msg)

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
        session['formdata'] = {}
        # request_body = {}
        # request_body["chart_title"] = request.form["chartTitle"] or ''

        session['formdata']['chart_title'] = request.form['chartTitle']

        print(session)

        try:
            file = request.files['inputFile']
        except KeyError:
            msg = Markup("<strong>Error:</strong> No file selected. Please provide a data file.")
            flash(msg, category='alert-danger')

            # TODO: log error to file
            return redirect(request.url)

        if file.filename == '' or not allowed_file(file.filename):
            msg = Markup("<strong>Error:</strong> Invalid file name. Please provide either .csv or .txt")
            flash(msg, category="alert-danger")
            return redirect(request.url)

        # All tests passed, we will save the file
        if file and allowed_file(file.filename):
            timestamp = int(round(time() * 1000))
            ext = os.path.splitext(file.filename)[1]

            session['formdata']['timestamp'] = timestamp
            session['formdata']['file_extension'] = ext

            filename = "{}{}".format(timestamp, ext)
            session['formdata']['file_name'] = filename
            # print("Filename: ", filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return redirect(url_for('statistics', timestamp=timestamp))
    # On GET Method
    return render_template("upload.html")


@app.route('/statistics/<int:timestamp>', methods=['GET'])
def statistics(timestamp):

    linear.main(timestamp=timestamp, request_body=session['formdata'])

    # asyncio.run(send_email(['email@googlemail.com']))
    return render_template("statistics.html", timestamp=timestamp)


@app.route('/chart/<int:timestamp>', methods=['GET'])
def chart(timestamp):
    path = 'charts/{}.png'.format(timestamp)
    return send_file(path, mimetype='image/png')

@app.route('/changelog')
def changelog():
    # Load Changelog.json and pass to template
    with open('app/changelog.json', 'r') as f:
        changelog=json.load(f)
        return render_template('changelog.html', changelog=changelog)

@app.route('/examples')
def examples():
    return render_template('examples.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def internal_server_error():
    return render_template("errors/500.html"), 500
