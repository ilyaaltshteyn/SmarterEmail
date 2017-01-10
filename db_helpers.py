import os
import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime

def runSQL(sql):
    if 'RDS_HOSTNAME' in os.environ:
        DATABASES = {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ['RDS_DB_NAME'],
                'USER': os.environ['RDS_USERNAME'],
                'PASSWORD': os.environ['RDS_PASSWORD'],
                'HOST': os.environ['RDS_HOSTNAME'],
                'PORT': os.environ['RDS_PORT']
                }

    with pymysql.connect(host = DATABASES['HOST'], user = DATABASES['USER'],
                         passwd = DATABASES['PASSWORD'], db = 'ebdb',
                         cursorclass=DictCursor) as cur:
        cur.execute("SELECT * FROM email_analysis_results")
        return cur.fetchall()
    #
    # """ Connects to db and executes sql. Returns one line of results. """
    #
    # with pymysql.connect(host = DATABASES['HOST'], user = DATABASES['USER'],
    #                      passwd = DATABASES['PASSWORD'], db = 'ebdb',
    #                      cursorclass=DictCursor) as cur:
    #     cur.execute(sql)
    #     return cur.fetchall()


def store_results(cookie_val, results):
    """ Formats + sends the results of the analyze.py Analyzer.analyze() func to sql. """

    if results and cookie_val:
        results = eval(results)

        insert_sql = "INSERT INTO email_analysis_results (cookie_id, record_datetime, emails_analyzed, avg_grade_lvl, avg_sentences, avg_syllables) VALUES ('{}', '{}', {}, {}, {}, {})"

        insert_sql = insert_sql.format(cookie_val, str(datetime.now()),
                     results['emails_analyzed'],
                     results['my_combined_grade_lvl_mean'],
                     results['sentence_count_mean'],
                     results['lexicon_count_mean'])

        print "SQL TO INSERT IS: ", insert_sql

        runSQL(insert_sql)

def get_averages():
    """ Retrieves average results for basic metrics. """

    averages_sql = "SELECT * FROM email_analysis_results"

    result = runSQL(averages_sql)
    print result
    return result
