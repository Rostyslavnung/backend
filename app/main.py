from flask import Flask, render_template

from app.api.api import api

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')