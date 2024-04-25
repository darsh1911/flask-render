import os
import json
import requests

from flask import Flask, render_template, request, json, session

import vendors
import leads
from flask_session import Session
from vendors import add_vendor

app = Flask(__name__)

app.config['RECAPTCHA_SITE_KEY'] = os.environ.get('RECAPTCHA_SITE_KEY')
app.config['RECAPTCHA_SECRET_KEY'] = os.environ.get('RECAPTCHA_SECRET_KEY')
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET_KEY')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)

@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/partners/register')
def partner_register():  # put application's code here
    # print(app.config['RECAPTCHA_SECRET_KEY'])
    return render_template('/partner/partner-registration.html')


@app.route('/partners/register/callback', methods=["POST"])
def partner_register_submit():
    if request.method == "POST":
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                          data={'secret': app.config['RECAPTCHA_SECRET_KEY'],
                                'response': request.form['recaptchaResponse']})
        google_response = json.loads(r.text)
        if google_response['success']:
            if google_response['score'] >= 0.7:
                result = add_vendor(request.form['name'], request.form['email'], (request.form['phone'].split(' '))[-1],
                                    request.form['company'], request.form['address'], request.form['city'],
                                    request.form['pincode'], request.form['staff'], request.form['password'])
                if result['success']:
                    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
                else:
                    return json.dumps(
                        {'success': False, 'error': str(result['error'])}), 200, {
                        'ContentType': 'application/json'}
            else:
                return json.dumps(
                    {'success': False, 'error': 'Bad Captcha | Score:' + str(google_response['score'])}), 200, {
                    'ContentType': 'application/json'}
        else:
            return json.dumps(
                {'success': False, 'error': 'Bad Captcha | Score:' + str(google_response['score'])}), 200, {
                'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False, 'error': 'Unknown Error Occured'}), 200, {
            'ContentType': 'application/json'}


@app.route('/partners/login/callback', methods=["POST"])
def partner_login_submit():
    if request.method == "POST":
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                          data={'secret': app.config['RECAPTCHA_SECRET_KEY'],
                                'response': request.form['recaptchaResponse']})
        google_response = json.loads(r.text)
        if google_response['success']:
            if google_response['score'] >= 0.7:
                login = vendors.login(email=request.form['email'], password=request.form['password'])
                if login['success'] is True:
                    session['id'] = login['id']
                    session['name'] = login['name']
                    return json.dumps({'success': True, 'error': 'Good login'}), 200, {
                        "ContentType": 'application/json'}
                else:
                    return json.dumps({'success': False, 'error': str(login['error'])}), 200, {
                        'ContentType': 'application/json'}
            else:
                return json.dumps(
                    {'success': False, 'error': 'Bad Captcha | Score:' + str(google_response['score'])}), 200, {
                    'ContentType': 'application/json'}
        else:
            return json.dumps(
                {'success': False, 'error': 'Bad Captcha' + str(google_response)}), 200, {
                'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False, 'error': 'Unknown Error Occured'}), 200, {
            'ContentType': 'application/json'}


@app.route('/partners/dashboard', methods=["GET"])
def partner_dashboard():
    return render_template('coming-soon.html')


@app.route('/services', methods=["GET"])
def services():
    return render_template('coming-soon.html')


@app.route('/subscribe', methods=["POST"])
def subscribe():
    if request.method == "POST":
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                          data={'secret': app.config['RECAPTCHA_SECRET_KEY'],
                                'response': request.form['recaptchaResponse']})
        google_response = json.loads(r.text)
        if google_response['success']:
            if google_response['score'] >= 0.7:
                result = leads.new_lead(email=request.form['email'])
                if result['success'] is True:
                    return json.dumps({'success': True, 'error': 'Subscribed successfully.'}), 200, {
                        "ContentType": 'application/json'}
                else:
                    return json.dumps({'success': False, 'error': str(result['error'])}), 200, {
                        'ContentType': 'application/json'}
            else:
                return json.dumps(
                    {'success': False, 'error': 'Bad Captcha | Score:' + str(google_response['score'])}), 200, {
                    'ContentType': 'application/json'}
        else:
            return json.dumps(
                {'success': False, 'error': 'Bad Captcha' + str(google_response)}), 200, {
                'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False, 'error': 'Unknown Error Occured'}), 200, {
            'ContentType': 'application/json'}


# app name
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found():
    # defining function
    return render_template("404.html")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
