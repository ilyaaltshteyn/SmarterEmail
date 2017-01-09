# This script wraps the GMAIL api. It assumes you're authenticated, have an
# access token and a first response from the gmail api.

from urllib2 import Request, urlopen, URLError
import base64
import email


class Gmail():
    """ Wraps gmail api. Its main function is run(), which retrieves all emails
        from the authenticated user's mailbox, along with some metainfo. """

    def __init__(self, first_response, access_token):

        self.allofit = eval(first_response)
        self.message_ids = self.allofit['messages']

        if 'nextPageToken' in self.allofit:
            self.nextPageToken = self.allofit['nextPageToken']
        else:
            self.nextPageToken = None

        self.headers = {'Authorization': 'OAuth ' + access_token}
        self.pagesCount = 0
        self.msgsCount = 0

        self.message_texts = []


    def decode_base64(self, data, possible_codecs = ['ascii', 'utf8']):
        """Decode base64, padding optional.

        :param data: Base64 data as an ASCII byte string
        :returns: The decoded byte string.

        """

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

        req = Request('https://www.googleapis.com/gmail/v1/users/me/messages?pageToken={}'.\
                      format(self.nextPageToken), None, self.headers)

        response_text = eval(urlopen(req).read())

        self.message_ids.extend(response_text['messages'])
        self.pagesCount += 1

        try:
            self.nextPageToken = response_text['nextPageToken']
        except KeyError:
            pass


    def get_message_txt(self, m_id):
        """ Retrieves the message with the given id. """

        try:
            req = Request('https://www.googleapis.com/gmail/v1/users/me/messages/{}?format=RAW'.format(m_id),
                          None, self.headers)

            response_text = eval(urlopen(req).read())
            self.msgsCount += 1
            print "Emails pulled: {}".format(self.msgsCount)

        except:
            return ''

        m = email.message_from_string(self.decode_base64(response_text['raw']))

        if m.is_multipart():
            # Doesn't support arbitrary num of recursive parts.
            for payload in m.get_payload():
                if payload.is_multipart():
                    for p in payload.get_payload():
                        return p.get_payload()
                else:
                    return payload.get_payload()

        else:
            return self.decode_base64(m.get_payload())


    def get(self):

        # Get a reasonable number of message ids:
        while self.nextPageToken and self.pagesCount <= 10:
            try:
                self.get_all_message_ids()
            except:
                pass

        # Get messages for those ids:
        self.message_ids = self.message_ids[:100] # snip for testing.

        for m_id in self.message_ids:
            try:
                self.message_texts.append(self.get_message_txt(m_id['id']))
            except:
                continue

        return self.message_texts
