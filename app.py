from flask import  Flask, render_template, request,Blueprint
from api.message import messageAPI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.register_blueprint(messageAPI)

@app.route('/')
def hello():
    return render_template('index.html')




app.run(os.getenv('HOST'), port=os.getenv('PORT'))