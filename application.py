from flask import Flask, Response, redirect, url_for, session, render_template
from flask_oauth import OAuth
from google_api_wrapper import Gmail
from urllib2 import Request, urlopen, URLError
from parse import GmailParser
from analyze import Analyzer

# ------------------------------------------------------------------------------
# Get from Google APIs console
# https://code.google.com/apis/console

# with open('/Users/ilya/Projects/SmarterEmail/secret_stuff.whats_this', 'rb') as infile:
#     lines = infile.readlines()

GOOGLE_CLIENT_ID = '631813692358-hqjmcu2skn4qlnk8rpoupom859cmfnje.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'F3AU6cy9JYFi6DTMS6WpSP0s'
REDIRECT_URI = '/oauth2callback'  # one of the Redirect URIs from Google APIs console


# ------------------------------------------------------------------------------

SECRET_KEY = 'development key'
DEBUG = True

application = Flask(__name__)
application.debug = DEBUG
application.secret_key = SECRET_KEY
oauth = OAuth()

google = oauth.remote_app('SmarterEmail',
                          base_url='https://www.googleapis.com/gmail/v1/users/me/messages',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/gmail.readonly',
                                                'response_type' : 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)

@application.route('/')
def index():
    return render_template('home.html')


@application.route('/authorize')
def authorize():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))

    return render_template('loading.html')


@application.route('/analyze')
def analyze():

    def t():
        yield """<!doctype html>
<title>Send javascript snippets demo</title>
<style>
  #data {
    text-align: center;
  }
</style>
<script src="http://code.jquery.com/jquery-latest.js"></script>
<div id="data">nothing received yet</div>
"""

        access_token = session.get('access_token')[0]

        from urllib2 import Request, urlopen, URLError

        headers = {'Authorization': 'OAuth '+access_token}

        print 'REQUESTING FIRST BATCH OF MSG IDS'
        req = Request('https://www.googleapis.com/gmail/v1/users/me/messages?q=from:me%20-in:chat%20-category:(promotions%20OR%20social)',
                      None, headers)

        try:
            res = urlopen(req)
        except URLError, e:
            print 'reason is... ', e.reason

            if e.code == 401:
                # Unauthorized - bad token
                session.pop('access_token', None)
                yield redirect(url_for('login'))

            all_messages = Gmail(res.read(), access_token).get()
            parsed_messages = GmailParser(all_messages).parse()
            results = str(Analyzer(parsed_messages).analyze())
            # return render_template('results.html', summary = results)

        all_messages = Gmail(res.read(), access_token).get()
        parsed_messages = GmailParser(all_messages).parse()
        results = str(Analyzer(parsed_messages).analyze())
        yield """<script>
      $("#data").text("{dat}")
    </script>
    """.format(dat=results)

    return Response(t())

    # return render_template('results.html', summary = results)

@application.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)



@application.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('authorize'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')


if __name__ == '__main__':
    application.run()
