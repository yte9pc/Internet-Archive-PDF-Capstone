import os
import sqlite3
import pandas as pd
from sqlite3 import Error
from google_trans_new import google_translator  

def create_connection(db):
    # Create database
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    return conn
        
def execute(conn,  table_sql, val = '', insert = False):
    # Create tables words, translate
    # And insert data into the tables
    try:
        c = conn.cursor()
        if insert == True:
            c.execute(table_sql, val)
            conn.commit()
        else:
            c.execute(table_sql)
    except Error as e:
        print(e)

def insertWords(conn, dictionary, langs,  iso):
    selectwords = "SELECT word FROM words"
    df = pd.read_sql_query(selectwords, conn)
    
    if len(df) == 0:
        for i in dictionary:
            for j in dictionary.get(i):
                wordInsert = "INSERT INTO words (word, type) VALUES (?, ?)"
                val = (j, i)
                execute(conn, wordInsert, val, insert = True)
        insertTranslate(conn, langs,  iso)
    
def insertTranslate(conn, langs,  iso):
    selectwords = "SELECT word, type FROM words"
    df = pd.read_sql_query(selectwords, conn)
    listofWords = df.word.values
    types = df.type.values
    
    translator = google_translator()  
    for word in range(len(listofWords)):
        for targetLang in range(len(iso)):
            if iso[targetLang] != 'en':
                translatej = translator.translate(listofWords[word], lang_src = 'en' , lang_tgt = iso[targetLang])
                if isinstance(translatej, list) == True:
                    translatej = ', '.join(translatej)
                    
                wordInsert = "INSERT INTO translate (eng_word, language, transl_iso, transl_word, type) VALUES (?, ?, ?, ?, ?)"
                val = (listofWords[word], langs[targetLang], iso[targetLang], str(translatej), types[word])
                execute(conn, wordInsert, val, insert = True)
                         
if __name__ == '__main__':
    conn = create_connection('googletranslate.db')

    if conn != None:
        # Create table sql
        words = """ CREATE TABLE IF NOT EXISTS words (
                                            word_id integer PRIMARY KEY AUTOINCREMENT,
                                            word text NOT NULL,
                                            type text NOT NULL
                                        ); """
        
        translate = """ CREATE TABLE IF NOT EXISTS translate (
                                            transl_id integer PRIMARY KEY AUTOINCREMENT,
                                            eng_word text NOT NULL,
                                            language text NOT NULL,
                                            transl_iso text NOT NULL,
                                            transl_word text NOT NULL,
                                            type text NOT NULL
                                        ); """
        execute(conn, words)
        execute(conn, translate)

        # Create an index on the translate table
        # Improves query time
        transl_index = """ CREATE INDEX idx_transl
                            ON translate 
                            (eng_word, transl_iso); """
        execute(conn, transl_index)
        
        # Insert words into words table
        struct = ['abstract', 'introduction', 'conclusion', 'reference', 'table of content']
        content = ['thesis', 'research', 'statistic', 'analyze', 'analysis', 'result', 'table', 
                   'investigation', 'explain', 'theory', 'study', 'paper', 'data', 'perform', 
                   'performance', 'hypothesis', 'discussion', 'experiment', 'method', 'methodology', 
                   'measurement', 'measure', 'surgery', 'average', 'survey']
        assoc = ['journal', 'association', 'assoc', 'organization', 'doi', 'university', 'school', 
                 'board', 'publish', 'author', 'publication', 'conference', 'conference proceedings', 'society']
        
        dictionaryWords = {'structure' : struct, 'content' : content, 'association' : assoc}
        
        # Insert translated words into translate table
        langs = ['Afrikaans', 'Albanian', 'Arabic', 'Bengali', 'Bulgarian',
           'Catalan', 'Croatian', 'Czech', 'Danish', 'Dutch', 'English',
           'Estonian', 'Finnish', 'French', 'German', 'Gujarati', 'Hebrew',
           'Hindi', 'Hungarian', 'Indonesian', 'Italian', 'Japanese',
           'Korean', 'Latvian', 'Lithuanian', 'Macedonian',
           'Modern Greek (1453-)', 'Nepali (macrolanguage)', 'Norwegian',
           'Persian', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Slovak',
           'Slovenian', 'Somali', 'Spanish', 'Swahili (macrolanguage)',
           'Swedish', 'Tagalog', 'Tamil', 'Thai', 'Turkish', 'Ukrainian',
           'Urdu', 'Vietnamese', 'Welsh']
        iso = ['af', 'sq', 'ar', 'bn', 'bg', 'ca', 'hr', 'cs', 'da', 'nl', 'en',
           'et', 'fi', 'fr', 'de', 'gu', 'he', 'hi', 'hu', 'id', 'it', 'ja',
           'ko', 'lv', 'lt', 'mk', 'el', 'ne', 'no', 'fa', 'pl', 'pt', 'ro',
           'ru', 'sk', 'sl', 'so', 'es', 'sw', 'sv', 'tl', 'ta', 'th', 'tr',
           'uk', 'ur', 'vi', 'cy']
        
        insertWords(conn, dictionaryWords, langs, iso)
        conn.close()