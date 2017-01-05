# This script has an Analyzer class which is initialized with a list of emails.
# The class can filter out unnecessary emails and run analyses on them.
from textstat.textstat import textstat as tstat
from pprint import pprint

class Analyzer():

    def __init__(self, emails):
        self.emails = emails
        self.lex_counts = []
        self.sent_counts = []
        self.flesch_scores = []
        self.flesch_kincaid_grades = []

    def analyze_one(self, email):
        """ Analyzes a single email. """
        # self.lex_counts.append(lexicon_count(email))
        print email
        print 'LEX COUNT: ', tstat.lexicon_count(email)
        # self.sent_counts.append(sentence_count(email))
        print 'SENT COUNT: ', tstat.sentence_count(email)
        # self.flesch_scores.append(flesch_reading_ease(email))
        print 'READING EASE: ', tstat.flesch_reading_ease(email)
        # self.flesch_kincaid_grades.append(flesch_kincaid_grade(email))
        print 'READING GRADE: ', tstat.flesch_kincaid_grade(email)

    def analyze(self):
        """ Analyzes all emails. """

        for em in self.emails:
            self.analyze_one(em)
