from flask import Flask, Response, redirect, url_for, session, render_template, request
from flask_oauth import OAuth
from google_api_wrapper import Gmail
from urllib2 import Request, urlopen, URLError
from parse import GmailParser
from analyze import Analyzer
from db_helpers import get_averages, store_results
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, SECRET_KEY

# ------------------------------------------------------------------------------

REDIRECT_URI = '/oauth2callback'

application = Flask(__name__)
application.debug = True
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

# ------------------------------------------------------------------------------


def stream_template(template_name, **context):
    """ Streams data to template while stuff happens back here. """

    application.update_template_context(context)
    t = application.jinja_env.get_template(template_name)

    return t.stream(context)


def get_first_response():
    """ Retrieves first set of results from gmail. """

    access_token = session.get('access_token')[0]

    headers = {'Authorization': 'OAuth ' + access_token}

    req = Request('https://www.googleapis.com/gmail/v1/users/me/messages?q=in:sent%20-in:chat', #%20-category:(promotions%20OR%20social)
                  None, headers)

    try:
        res = urlopen(req)
    except URLError, e:
        print 'reason is... ', e.reason
        session.pop('access_token', None)
        return redirect(url_for('login'))

    return res.read()


def analyze():
    """ Gets data, analyzes it, streams it to template. """

    access_token = session.get('access_token')[0]
    first_response = get_first_response()

    def run(first_response, access_token):

        all_messages = Gmail(first_response, access_token).get()
        parsed_messages = GmailParser(all_messages).parse()
        results = str(Analyzer(parsed_messages).analyze())

        try:
            # Pull data to show in results before storing new data in db:
            avgs = get_averages()
            store_results(cookie, results)
        except:
            avgs = {'avg_grade_lvl' : 'unknown',
                    'avg_sentences' : 'unknown',
                    'avg_syllables' : 'unknown',
                    'n' : 'unknown'}

        yield (results, avgs)

    return Response(stream_template('results2.html', data = run(first_response,
                                                                access_token)))

@application.route('/')
def index():
    return render_template('home.html')


@application.route('/authorize')
def authorize():
    # Grab cookie here bc you can be sure it's been set in browser already:
    global cookie
    cookie = request.cookies.get('smartrEmailVisit')

    if not session.get('access_token'):
        return redirect(url_for('login'))

    return analyze()


@application.route('/login')
def login():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback = callback)


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
