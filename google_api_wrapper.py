# This script wraps the GMAIL api. It assumes you're authenticated, have an
# access token and a first response from the gmail api.

from urllib2 import Request, urlopen, URLError
import base64, quopri, email, binascii

class Gmail():
    """ Wraps gmail api. Its main function is run(), which retrieves all emails
        from the authenticated user's mailbox, along with some metainfo. """

    def __init__(self, first_response, access_token):
        print 'initializing gmail class'

        self.allofit = eval(first_response)
        self.message_ids = self.allofit['messages']
        self.nextPageToken = self.allofit['nextPageToken']
        self.nextPageExists = True if self.nextPageToken else False

        self.headers = {'Authorization': 'OAuth ' + access_token}
        self.pagesCount = 0
        self.msgsCount = 0
        self.message_texts = []


    def decode_base64(self, data):
        """Decode base64, padding being optional.

        :param data: Base64 data as an ASCII byte string
        :returns: The decoded byte string.

        """
        # data = data.encode('ascii')

        missing_padding = len(data) % 4
        if missing_padding != 0:
            data += b'='* (4 - missing_padding)

        decoded = base64.urlsafe_b64decode(data)

        return decoded


    def get_all_message_ids(self):
        # IN THE FUTURE: MAKE THIS RECURSIVE SO YOU DON'T HAVE TO COUNT.
        print 'INSIDE get_all_message_ids func now'

        req = Request('https://www.googleapis.com/gmail/v1/users/me/messages?pageToken={}'.format(self.nextPageToken),
                      None, self.headers)

        response_text = eval(urlopen(req).read())

        self.message_ids.extend(response_text['messages'])
        self.pagesCount += 1

        try:
            self.nextPageToken = response_text['nextPageToken']
        except KeyError:
            self.nextPageExists = False

        if self.pagesCount > 0:
            self.nextPageExists = False


    def get_message_txt(self, m_id):
        """ Retrieves the message with the given id. """

        print 'INSIDE get_message_txt func now'

        try:
            req = Request('https://www.googleapis.com/gmail/v1/users/me/messages/{}?format=RAW'.format(m_id),
                          None, self.headers)

            response_text = eval(urlopen(req).read())
            self.msgsCount += 1
            print "100s of emails: {},    Emails pulled: {}".format(self.pagesCount,
                                                                    self.msgsCount)
        except:
            return 'api hit failure from get_message_txt function'


        try:
            print 'inside try except in get_message'
            # print response_text['raw']
            m = email.message_from_string(self.decode_base64(response_text['raw']))
            if m.is_multipart():
                for payload in m.get_payload():
                    # if payload.is_multipart(): ...
                    print 'HERE 1'
                    print self.decode_base64(payload.get_payload(decode = True)).encode('utf8')
            else:
                print 'HERE 1a'
                print self.decode_base64(m.get_payload(decode = True)).encode('utf8')
                print 'HERE 2'

        except Exception, e:
            print e
            print 'HERE 3'
            return 'FAILED TO FIND payload, or something else went wrong.'


    def get(self):
        print 'inside get func now'

        while self.nextPageExists:
            self.get_all_message_ids()

        # Get all messages:
        print 'Getting all messages'
        for m_id in self.message_ids:
            self.message_texts.append(self.get_message_txt(m_id['id']))

        return self.message_texts
