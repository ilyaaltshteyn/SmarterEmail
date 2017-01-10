from flask import Flask, Response, redirect, url_for, session, render_template
from flask_oauth import OAuth
from google_api_wrapper import Gmail
from urllib2 import Request, urlopen, URLError
from parse import GmailParser
from analyze import Analyzer
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, SECRET_KEY
import os
import pymysql

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

REDIRECT_URI = '/oauth2callback'

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


if 'RDS_HOSTNAME' in os.environ:
    DATABASES = {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT']
            }

try:
    print DATABASES
except:
    print 'NO DB FOUND'


conn = pymysql.connect(host = DATABASES['HOST'], user = DATABASES['USER'],
                       passwd = DATABASES['PASSWORD'], db = 'ebdb')
cur = conn.cursor()
cur.execute("SELECT Host,User FROM user")
print(cur.description)
print()

for row in cur:
    print(row)

cur.close()
conn.close()

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


def stream_template(template_name, **context):
    """ Streams data to template. """

    application.update_template_context(context)
    t = application.jinja_env.get_template(template_name)
    rv = t.stream(context)
    return rv


def analyze():
    """ Gets data and analyzes it, then streams it to template. """

    access_token = session.get('access_token')[0]

    from urllib2 import Request, urlopen, URLError

    headers = {'Authorization': 'OAuth '+access_token}

    print 'REQUESTING FIRST BATCH OF MSG IDS'
    req = Request('https://www.googleapis.com/gmail/v1/users/me/messages?q=in:sent%20-in:chat', #%20-category:(promotions%20OR%20social)
                  None, headers)


    try:
        res = urlopen(req)
    except URLError, e:
        print 'reason is... ', e.reason

        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))

    first_response = res.read()

    def t(first_response, access_token):

        all_messages = Gmail(first_response, access_token).get()
        parsed_messages = GmailParser(all_messages).parse()
        results = str(Analyzer(parsed_messages).analyze())

        yield results

    return Response(stream_template('results.html', data = t(first_response, access_token)))


@application.route('/')
def index():
    return render_template('home.html')


@application.route('/authorize')
def authorize():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))

    return analyze()


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
