
# Tools to parse lists of raw but decoded emails returned by the Gmail class.

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
        self.msgs_parsed = []

    def parse_one(self, msg):
        """ Strips links from a single Gmail message, then parses it. """

        msg_delinked = strip_tags(msg)

        up_to_reply = r'(?:(?!On (Mon |Tue |Wed |Thu |Fri |Sat |Sun |Mon, |Tue, |Wed, |Thu, |Fri, |Sat, |Sun, ))[\s\S])*'
        up_to_carrot = r'.+?(?=>)'

        match = re.search(up_to_reply, msg_delinked)

        if match:
            return match.group()

        match2 = re.search(up_to_carrot, msg)

        if match2:
            return match2.group()

        return ''


    def parse(self):
        """ Runs self.parse_one() on all messages."""

        for m in self.messages:
            try:
                self.msgs_parsed.append(self.parse_one(m))
            except:
                continue

        return self.msgs_parsed
