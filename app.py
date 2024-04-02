import os
import json
import requests
from flask import Flask, render_template, request, json

app = Flask(__name__)
app.config['RECAPTCHA_SITE_KEY'] = os.environ.get('RECAPTCHA_SITE_KEY')
app.config['RECAPTCHA_SECRET_KEY'] = os.environ.get('RECAPTCHA_SECRET_KEY')


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/partners/register')
def partner_register():  # put application's code here
    print(app.config['RECAPTCHA_SECRET_KEY'])
    return render_template('/partner/partner-registration.html')


@app.route('/partners/register/callback', methods=["POST"])
def gfg():
    if request.method == "POST":
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                          data={'secret': app.config['RECAPTCHA_SECRET_KEY'],
                                'response': request.form['recaptchaResponse']})
        google_response = json.loads(r.text)
        if google_response['success']:
            if google_response['score'] >= 0.7:
                return json.dumps({'success': False, 'error': 'Good Captcha | Score:' + str(google_response['score'])}), 200, {'ContentType': 'application/json'}
            else:
                return json.dumps({'success': False, 'error': 'Bad Captcha | Score:' + str(google_response['score'])}), 200, {'ContentType': 'application/json'}
        else:
            # FAILED
            print('FAILED')
#    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


# app name
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found():
    # defining function
    return render_template("templates/404.html")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
