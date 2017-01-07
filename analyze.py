from textstat.textstat import textstat as tstat
import numpy as np
import re
from collections import Counter
# from talon.signature.bruteforce import extract_signature


class Analyzer():

    def __init__(self, emails):
        self.emails = emails

        #Individual msg metrics using tstat:
        self.lexicon_count = []
        self.sentence_count = []
        self.flesch_reading_ease = []
        self.flesch_kincaid_grade = []
        self.gunning_fog = []
        self.smog_index = []
        self.automated_readability_index = []
        self.coleman_liau_index = []
        self.linsear_write_formula = []
        self.dale_chall_readability_score = []

        # Individual msg metrics using regex:
        self.introductions = []
        self.signoffs = []


    def preprocess(self, email):
        if email:
            e = email.replace('\t', '').replace('\n', ' ').replace('\r', ' ')
            return e.strip(' \t\n\r')


    def analyze_one(self, email):
        """ Analyzes a single email. """

        self.lexicon_count.append(tstat.lexicon_count(email))
        self.sentence_count.append(tstat.sentence_count(email))
        self.flesch_reading_ease.append(tstat.flesch_reading_ease(email))
        self.flesch_kincaid_grade.append(tstat.flesch_kincaid_grade(email))
        self.gunning_fog.append(tstat.gunning_fog(email))
        self.smog_index.append(tstat.smog_index(email))
        self.automated_readability_index.append(tstat.automated_readability_index(email))
        self.coleman_liau_index.append(tstat.coleman_liau_index(email))
        self.linsear_write_formula.append(tstat.linsear_write_formula(email))
        self.dale_chall_readability_score.append(tstat.dale_chall_readability_score(email))

        # self.signoffs.append(self.preprocess(extract_signature(email)[1]))

        # Get start and end if there are >2 sentence chunks in the msg.
        sents = [s.lower() for s in re.split(r'(?<=[.:;,!?])(\n|\s|\r)', email)]

        if len(sents) > 2:
            self.introductions.append(self.preprocess(sents[0]))
            self.signoffs.extend([self.preprocess(c) for c in sents[-2:]] )


    def combine_scores(self):
        """ Takes the mean of grade level estimates from tstat. """

        return np.mean((np.mean(self.flesch_kincaid_grade),
                       np.mean(self.automated_readability_index),
                       np.mean(self.coleman_liau_index),
                       np.mean(self.linsear_write_formula),
                       np.mean(self.dale_chall_readability_score) ))


    def get_common(self, lst, n = 15):
        """ Finds n most common list elements (can be used on introductions and
            signoffs). """

        data = Counter(lst)
        return [x for x in data.most_common(n) if x[0]]


    def analyze(self):
        """ Analyzes all emails and returns summary stats. """

        for e in self.emails:
            self.analyze_one(e)

        # print self.emails

        dat = { 'lexicon_count_mean' : np.mean(self.lexicon_count),
                'lexicon_count_range' : (np.min(self.lexicon_count),
                                        np.max(self.lexicon_count)),
                'lexicon_count_std' : np.std(self.lexicon_count),

                'sentence_count_mean' : np.mean(self.sentence_count),
                'sentence_count_range' : (np.min(self.sentence_count),
                                         np.max(self.sentence_count)),
                'sentence_count_std' : np.std(self.sentence_count),

                'flesch_reading_ease_mean' : np.mean(self.flesch_reading_ease),
                'flesch_reading_ease_range' : (np.min(self.flesch_reading_ease),
                                              np.max(self.flesch_reading_ease)),
                'flesch_reading_ease_std' : np.std(self.flesch_reading_ease),

                'flesch_kincaid_grade_mean' : np.mean(self.flesch_kincaid_grade),
                'flesch_kincaid_grade_range' : (np.min(self.flesch_kincaid_grade),
                                               np.max(self.flesch_kincaid_grade)),
                'flesch_kincaid_grade_std' : np.std(self.flesch_kincaid_grade),

                'gunning_fog_mean' : np.mean(self.gunning_fog),
                'smog_index_mean' : np.mean(self.smog_index),
                'automated_readability_index_mean' : np.mean(self.automated_readability_index),
                'coleman_liau_index_mean' : np.mean(self.coleman_liau_index),
                'linsear_write_formula_mean' : np.mean(self.linsear_write_formula),
                'dale_chall_readability_score_mean' : np.mean(self.dale_chall_readability_score),

                'my_combined_grade_lvl_mean' : self.combine_scores(),

                'most_common_intros' : self.get_common(self.introductions),
                'most_common_signoffs' : self.get_common(self.signoffs),

                'emails_analyzed' : len(self.emails)
               }

        return str(dat)
