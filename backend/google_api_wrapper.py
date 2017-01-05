# This script wraps the GMAIL api. It assumes you're authenticated, have an
# access token and a first response from the gmail api.

from urllib2 import Request, urlopen, URLError
import base64, quopri, email, binascii


class Gmail():
    """ Wraps gmail api. Its main function is run(), which retrieves all emails
        from the authenticated user's mailbox, along with some metainfo. """

    def __init__(self, first_response, access_token):

        self.allofit = eval(first_response)
        self.message_ids = self.allofit['messages']
        self.nextPageToken = self.allofit['nextPageToken']
        self.nextPageExists = True if self.nextPageToken else False

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

        # IN THE FUTURE: MAKE THIS RECURSIVE SO YOU DON'T HAVE TO COUNT.


        req = Request('https://www.googleapis.com/gmail/v1/users/me/messages?pageToken={}'.format(self.nextPageToken),
                      None, self.headers)

        response_text = eval(urlopen(req).read())

        self.message_ids.extend(response_text['messages'])
        self.pagesCount += 1

        try:
            self.nextPageToken = response_text['nextPageToken']
        except KeyError:
            self.nextPageExists = False

        if self.pagesCount > 0 or self.msgsCount > 20:
            self.nextPageExists = False


    def get_message_txt(self, m_id):
        """ Retrieves the message with the given id. """

        try:
            req = Request('https://www.googleapis.com/gmail/v1/users/me/messages/{}?format=RAW'.format(m_id),
                          None, self.headers)

            response_text = eval(urlopen(req).read())
            self.msgsCount += 1
            print "100s of emails: {},    Emails pulled: {}".format(self.pagesCount,
                                                                    self.msgsCount)
        except:
            return 'api hit failure from get_message_txt function'


        m = email.message_from_string(self.decode_base64(response_text['raw']))
        if m.is_multipart():

            # MAKE THIS PART RECURSIVE!!!!

            for payload in m.get_payload():
                if payload.is_multipart():
                    for p in payload.get_payload():
                        return p.get_payload()
                else:
                    return payload.get_payload()
        else:
            return self.decode_base64(m.get_payload())


    def get(self):

        while self.nextPageExists:
            try:
                self.get_all_message_ids()
            except:
                pass

        # Get all messages:
        print 'Getting all messages'
        for m_id in self.message_ids:
            if self.msgsCount > 20:
                return self.message_texts
            try:
                self.message_texts.append(self.get_message_txt(m_id['id']))
            except:
                continue

        return self.message_texts
