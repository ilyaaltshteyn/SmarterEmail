from urllib2 import Request, urlopen
import base64
import email


class Gmail():
    """ Wraps gmail api to easily get mail from the authenticated user's sent
        messages folder. Assumes you're authenticated, have an access token and
        a first response from the gmail api. """

    def __init__(self, first_response, access_token):
        self.first_resp = eval(first_response)
        self.message_ids = self.first_resp['messages']

        if 'nextPageToken' in self.first_resp:
            self.page_token = self.first_resp['nextPageToken']
        else:
            self.page_token = None

        self.headers = {'Authorization': 'OAuth ' + access_token}
        self.pagesCount = 0
        self.msgsCount = 0

        self.message_texts = []


    def decode_base64(self, data, possible_codecs = ['ascii', 'utf8']):
        """ Decodes base64, padding optional. """
        missing_padding = len(data) % 4
        if missing_padding != 0:
            data += b'='* (4 - missing_padding)

        decoded = base64.urlsafe_b64decode(data)

        for i in possible_codecs:
            try:
                return decoded.decode(i).encode('ascii')
            except:
                pass

        return ''.encode('ascii')


    def get_all_message_ids(self):
        url = 'https://www.googleapis.com/gmail/v1/users/me/messages?pageToken={}'
        req = Request(url.format(self.page_token), None, self.headers)

        response = eval(urlopen(req).read())

        self.message_ids.extend(response['messages'])
        self.pagesCount += 1

        try:
            self.page_token = response['nextPageToken']
        except KeyError:
            self.page_token = None


    def get_message_txt(self, m_id):
        """ Retrieves the message with the given id. """
        try:
            url = 'https://www.googleapis.com/gmail/v1/users/me/messages/{}?format=RAW'
            req = Request(url.format(m_id), None, self.headers)

            response = eval(urlopen(req).read())
            self.msgsCount += 1
            print "Emails pulled: {}".format(self.msgsCount)

        except:
            return ''

        m = email.message_from_string(self.decode_base64(response['raw']))

        if m.is_multipart(): # This sucks, refactor w recursion
            for payload in m.get_payload():
                if payload.is_multipart():
                    for p in payload.get_payload():
                        return p.get_payload()
                else:
                    return payload.get_payload()

        else:
            return self.decode_base64(m.get_payload())


    def get(self):
        # Get 10 pages of message ids:
        while self.page_token and self.pagesCount <= 10:
            try:
                self.get_all_message_ids()
            except:
                pass

        self.message_ids = self.message_ids[:200] # snip for testing.

        # Get messages for those ids:
        for m_id in self.message_ids:
            try:
                self.message_texts.append(self.get_message_txt(m_id['id']))
            except:
                continue

        return self.message_texts
