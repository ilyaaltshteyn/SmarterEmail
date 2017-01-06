from textstat.textstat import textstat as tstat
import numpy as np

class Analyzer():

    def __init__(self, emails):
        self.emails = emails

        # Metrics, named after tstat functions:
        self.lexicon_count = []
        self.sentence_count = []
        self.flesch_reading_ease = []
        self.flesch_kincaid_grade = []

    def analyze_one(self, email):
        """ Analyzes a single email. """

        self.lexicon_count.append(tstat.lexicon_count(email))
        self.sentence_count.append(tstat.sentence_count(email))
        self.flesch_reading_ease.append(tstat.flesch_reading_ease(email))
        self.flesch_kincaid_grade.append(tstat.flesch_kincaid_grade(email))


    def analyze(self):
        """ Analyzes all emails and returns summary stats. """

        for e in self.emails:
            self.analyze_one(e)

        # print self.emails

        return """Avg word count: {0}, Word count range: {1}, Word count std: {2}
                 Avg sent count: {3}, Sent count range: {4}, Sent count std: {5}
                 Avg reading ease: {6}, Reading ease range: {7}, Reading ease std: {8}
                 Avg grade level: {9}, Grade level range: {10}, Grade level std: {11}
                 That's after analyzing {12} emails.
                 """.format(np.mean(self.lexicon_count),
                            (np.min(self.lexicon_count), np.max(self.lexicon_count)),
                            np.std(self.lexicon_count),

                            np.mean(self.sentence_count),
                            (np.min(self.sentence_count), np.max(self.sentence_count)),
                            np.std(self.sentence_count),

                            np.mean(self.flesch_reading_ease),
                            (np.min(self.flesch_reading_ease), np.max(self.flesch_reading_ease)),
                            np.std(self.flesch_reading_ease),

                            np.mean(self.flesch_kincaid_grade),
                            (np.min(self.flesch_kincaid_grade), np.max(self.flesch_kincaid_grade)),
                            np.std(self.flesch_kincaid_grade),

                            len(self.emails) )
