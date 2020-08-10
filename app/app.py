import sys
parent_dir = "\\".join(sys.path[0].split("\\")[:-1])
sys.path.append(parent_dir)

from flask import Flask, render_template, redirect, url_for, request
from forms import UsernameForm
import utils.modeling_utils as mu
import pandas as pd
import joblib
from dotenv import load_dotenv

import os

import berserk
from requests_oauthlib import OAuth2Session

load_dotenv(".env")
client_id = os.environ.get("CLIENT_ID")

session = OAuth2Session(client_id)
client = berserk.Client(session)

rf = joblib.load("rf.joblib")

app = Flask(__name__)

app.config['SECRET_KEY'] = '727y327273'

@app.route("/", methods=['GET', 'POST'])
def input():
    form = UsernameForm()
    if form.validate_on_submit():
        return redirect(url_for('results', white_username=form.white.data,
                        black_username=form.black.data, evaluation = form.evaluation.data,
                        white_clock = form.white_clock.data,
                        black_clock = form.black_clock.data, perf = form.perf.data))
    return render_template('home.html', post='Be', form=form)

@app.route("/results", methods=['GET', 'POST'])
def results():
    white = request.args.get("white_username")
    black = request.args.get("black_username")
    evaluation = request.args.get("evaluation")
    white_clock = request.args.get("white_clock")
    black_clock = request.args.get("black_clock")
    perf = request.args.get("perf")

    white_info = client.users.get_public_data(white)
    black_info = client.users.get_public_data(black)

    print(white_info)
    data = pd.Series()
    data = mu.transform(data, white_info, black_info, evaluation, white_clock, black_clock, perf)

    probs = rf.predict_proba([data])[0]

    return render_template('results.html',
                            white_info=white_info,
                            black_info=black_info,
                            white_prob="{:.2f}".format(probs[0]),
                            black_prob="{:.2f}".format(probs[1]))

@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html')

@app.route("/about/v1-0-0", methods=['GET'])
def aboutv1():
    return render_template('about.html')

@app.route("/about/v2-0-0", methods=['GET'])
def aboutv2():
    return render_template('about.html')

if __name__=='__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
