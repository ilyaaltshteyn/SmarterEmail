# This script wraps the GMAIL api. It assumes you're authenticated, have an
# access token and a first response from the gmail api.

from urllib2 import Request, urlopen, URLError

class Gmail():

    def __init__(self, first_response, access_token):
        self.allofit = eval(first_response)
        self.messages = self.allofit['messages']
        self.nextPageToken = self.allofit['nextPageToken']
        self.access_token = access_token
        self.nextPageExists = True if self.nextPageToken else False
        self.pagesCount = 0


    def get_all_message_ids(self):
        # IN THE FUTURE: MAKE THIS RECURSIVE SO YOU DON'T HAVE TO COUNT.

        headers = {'Authorization': 'OAuth ' + self.access_token}
        req = Request('https://www.googleapis.com/gmail/v1/users/me/messages?pageToken={}'.format(self.nextPageToken),
                      None, headers)

        res = urlopen(req)
        response_text = eval(res.read())
        self.messages.extend(response_text['messages'])
        self.pagesCount += 1

        try:
            self.nextPageToken = response_text['nextPageToken']
        except KeyError:
            self.nextPageExists = False

        if self.pagesCount > 3:
            self.nextPageExists = False


    def get(self):
        while self.nextPageExists:
            self.get_all_message_ids()

        return str(self.messages)
