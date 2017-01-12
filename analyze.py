from textstat.textstat import textstat as tstat
import numpy as np
import json


class Analyzer():

    def __init__(self, emails):

        self.emails = emails

        self.lex_count = []
        self.sent_count = []
        self.flesch_kincaid_grade = []
        self.automated_readability_index = []
        self.coleman_liau_index = []
        self.linsear_write_formula = []
        self.dale_chall_readability_score = []


    def analyze_one(self, email):
        """ Analyzes a single email and stores results. """

        self.lex_count.append(tstat.lexicon_count(email))
        self.sent_count.append(tstat.sentence_count(email))

        if email and len(email) > 0:
            self.flesch_kincaid_grade.append(tstat.flesch_kincaid_grade(email))
            self.automated_readability_index.append(tstat.automated_readability_index(email))
            self.coleman_liau_index.append(tstat.coleman_liau_index(email))
            self.linsear_write_formula.append(tstat.linsear_write_formula(email))
            self.dale_chall_readability_score.append(tstat.dale_chall_readability_score(email))


    def combine_scores(self):
        """ Produces a composite grade level score. """

        scores = []
        for s in [self.flesch_kincaid_grade, self.automated_readability_index,
                  self.coleman_liau_index, self.linsear_write_formula,
                  self.dale_chall_readability_score]:

            scores.extend([g for g in s if g < 18])

        print scores
        return np.mean(scores)


    def analyze(self):

        for e in self.emails:
            try:
                self.analyze_one(e)
            except:
                pass

        dat = { 'sentence_count_mean' : np.mean(self.sent_count),
                'sentence_counts' : self.sent_count,
                'my_combined_grade_lvl_mean' : self.combine_scores(),
                'emails_analyzed' : len(self.emails)
               }

        return str(json.dumps(dat))
