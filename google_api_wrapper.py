# This script wraps the GMAIL api. It assumes you're authenticated, have an
# access token and a first response from the gmail api.

from urllib2 import Request, urlopen, URLError
import base64, quopri, email

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
            print 'inside try exceptin get_message'

            m = email.message_from_string(unicode(response_text['raw'], 'utf-8'))
            if m.is_multipart():
                for payload in m.get_payload():
                    # if payload.is_multipart(): ...
                    print base64.b64decode(payload.get_payload(decode = True))
            else:
                print base64.b64decode(m.get_payload(decode = True))

        except:
            return 'FAILED TO FIND payload, or something else went wrong.'

    def get_all_msgs(self):
        print 'inside get_all_msgs func now'

        for m_id in self.message_ids:
            self.message_texts.append(self.get_message_txt(m_id['id']))

    def get(self):
        print 'inside get func now'

        while self.nextPageExists:
            self.get_all_message_ids()

        self.get_all_msgs()
        # print self.get_message(self.message_ids[0]['id'])

        return str(self.message_texts)#str(self.message_ids)
