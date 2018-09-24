import os

SECRET_KEY          = os.getenv('SECRET_KEY')

UPLOAD_FOLDER       = 'app/uploads'
CHART_FOLDER        = 'app/charts'
MAX_CONTENT_PATH    = 4096
MAX_FILE_SIZE       = 4096
ALLOWED_EXTENSIONS  = set(['txt', 'csv'])

# Mail Settings
MAIL_SERVER         = 'smtp.gmail.com'
MAIL_PORT           = 587
MAIL_USE_TLS        = True
MAIL_USE_SSL        = False
MAIL_USERNAME       = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD       = os.getenv('MAIL_PASSWORD')
