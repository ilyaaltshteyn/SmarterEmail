# This script has an Analyzer class which is initialized with a list of emails.
# The class can filter out unnecessary emails and run analyses on them.
from textstat.textstat import textstat as tstat
from pprint import pprint
import numpy as np

class Analyzer():

    def __init__(self, emails):
        self.emails = emails
        self.lex_counts = []
        self.sent_counts = []
        self.flesch_scores = []
        self.flesch_kincaid_grades = []

    def analyze_one(self, email):
        """ Analyzes a single email. """

        # FOR TESTING: (it works!)
        # print email
        # print 'LEX COUNT: ', tstat.lexicon_count(email)
        # print 'SENT COUNT: ', tstat.sentence_count(email)
        # print 'READING EASE: ', tstat.flesch_reading_ease(email)
        # print 'READING GRADE: ', tstat.flesch_kincaid_grade(email)

        self.lex_counts.append(tstat.lexicon_count(email))
        self.sent_counts.append(tstat.sentence_count(email))
        self.flesch_scores.append(tstat.flesch_reading_ease(email))
        self.flesch_kincaid_grades.append(tstat.flesch_kincaid_grade(email))

    def analyze(self):
        """ Analyzes all emails and returns summary stats. """

        for em in self.emails:
            self.analyze_one(em)

        print """Average word count: {0}, Word count range: {1}, Word count std: {2}
                 Average sent count: {3}, Sent count range: {4}, Sent count std: {5}
                 Average reading ease: {6}, Reading ease range: {7}, Reading ease std: {8}
                 Average grade level: {9}, Grade level range: {10}, Grade level std: {11}
                 """.format(np.mean(self.lex_counts),
                            (np.min(self.lex_counts), np.max(self.lex_counts)),
                            np.std(self.lex_counts),
                            np.mean(self.sent_counts),
                            (np.min(self.sent_counts), np.max(self.sent_counts)),
                            np.std(self.sent_counts),
                            np.mean(self.flesch_scores),
                            (np.min(self.flesch_scores), np.max(self.flesch_scores)),
                            np.std(self.flesch_scores),
                            np.mean(self.flesch_kincaid_grades),
                            (np.min(self.flesch_kincaid_grades), np.max(self.flesch_kincaid_grades)),
                            np.std(self.flesch_kincaid_grades))
