# This is a class that parses each message in a list of messages retrieved by
# the Gmail class.
import re

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class GmailParser():

    def __init__(self, messages):
        self.messages = messages

    def parse_one(self, msg):
        """ Parses a single Gmail message. """

        # Strip links first:
        msg_delinked = strip_tags(msg)

        up_to_reply = r'(?:(?!On (Mon |Tue |Wed |Thu |Fri |Sat |Sun |Mon, |Tue, |Wed, |Thu, |Fri, |Sat, |Sun, ))[\s\S])*'
        up_to_carrot = r'.+?(?=>)'

        match = re.search(up_to_reply, msg_delinked)

        if match:
            return 'MY EMAIL: {}, \n\n\n\n\n Raw email: {}'.format(match.group(), msg)
        else:
            match2 = re.search(up_to_carrot, msg)
            if match2:
                return 'MY EMAIL: {} \n\n\n\n\n Raw email: {}'.format(match2.group(), msg)
            else:
                return 'RAW EMAIL: ', msg

    def parse(self):
        """ Runs self.parse_one() on all messages in the list. """
        for m in self.messages:
            print self.parse_one(m)
