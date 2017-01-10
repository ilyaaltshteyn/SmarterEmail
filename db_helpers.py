import os
import pymysql
from datetime import datetime

def runSQL(sql):
    """ Connects to db and executes sql. Returns one line of results. """

    if 'RDS_HOSTNAME' in os.environ:
        DATABASES = {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ['RDS_DB_NAME'],
                'USER': os.environ['RDS_USERNAME'],
                'PASSWORD': os.environ['RDS_PASSWORD'],
                'HOST': os.environ['RDS_HOSTNAME'],
                'PORT': os.environ['RDS_PORT']
                }

    conn = pymysql.connect(host = DATABASES['HOST'], user = DATABASES['USER'],
                           passwd = DATABASES['PASSWORD'], db = 'ebdb')

    data = []
    with conn.cursor() as cur:
        cur.execute(sql)
        result = cur.fetchone()

    conn.close()
    return result


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

    averages_sql = "SELECT avg(avg_grade_lvl) avg_grade_lvl, avg(avg_sentences) avg_sentences, avg(avg_syllables) avg_syllables FROM ( SELECT cookie_id, avg(avg_grade_lvl) avg_grade_lvl, avg(avg_sentences) avg_sentences, avg(avg_syllables) avg_syllables FROM email_analysis_results GROUP BY cookie_id ) a"

    result = runSQL(averages_sql)
    print result
    return result
