
from time import time
from config import ALLOWED_EXTENSIONS


def allowed_file(filename):
    """
    Checks if the file extension is a valid one.
    Currently supported are '.csv' and '.txt'
    """
    return "." in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_milliseconds_since_epoch():
    """ Returns milliseconds elapsed since Jan 01 1970. """
    return int(round(time() * 1000))

def purge_uploads_folder():
    # Do this via cron or everytime a chart has been generated?
    pass