from flask import Flask

app = Flask(__name__)

app.secret_key = "7523"
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'jacobhobbs02@outlook.com'
app.config['MAIL_PASSWORD'] = 'AbbyJacob02'

