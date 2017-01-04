# This is a class that parses each message in a list of messages retrieved by
# the Gmail class.
import re

class GmailParser():

    def __init__(self, messages):
        self.messages = messages

    def parse_one(self, msg):
        """ Parses a single Gmail message. """

        # Strip links first:
        gmail_link = r'<https:(.*)>'
        msg = re.sub(gmail_link, '', msg)

        up_to_reply = r'(?:(?!On (Mon |Tue |Wed |Thu |Fri |Sat |Sun ))[^(>)])*'
        up_to_carrot = r'.+?(?=>)'

        match = re.search(up_to_reply, msg)

        if match:
            return 'MY EMAIL: {}'.format(match.group())
        else:
            match2 = re.search(up_to_carrot, msg)
            if match2:
                return 'MY EMAIL: {}'.format(match2.group())
            else:
                return 'RAW EMAIL: ', msg

    def parse(self):
        """ Runs self.parse_one() on all messages in the list. """
        for m in self.messages:
            print self.parse_one(m)
