import json
import sqlite3
from utils import Krypto as kr
import streamlit as st
import os
import sqlite3


class CRUD:
    # Constructor
    def __init__(self):
        self.conn = sqlite3.connect("AAP.db")
        self.cursor = self.conn.cursor()
        query = "CREATE TABLE IF NOT EXISTS appusers (id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT, password TEXT,admission_features TEXT, placement_features TEXT, Training_Mode_Admission TEXT DEFAULT NULL,Training_Mode_Placement TEXT DEFAULT NULL)"
        self.cursor.execute(query)
        self.conn.commit()

    def insert_user(self, email, password):
        query = "insert into appusers (email,password) values (?,?)"
        self.cursor.execute(query, (kr.hash_generator(
            email), kr.hash_generator(password)))
        self.conn.commit()

    def check_user_for_login(self, email, paasword):
        query = "select * from appusers where email=? and password=?"
        result = self.cursor.execute(query, (kr.hash_generator(
            email), kr.hash_generator(paasword))).fetchall()
        self.conn.commit()
        if result:
            return True
        else:
            return False

    def check_user_for_signup(self, email):
        query = "select * from appusers where email=?"
        result = self.cursor.execute(query, (kr.hash_generator(email),))
        self.conn.commit()
        if result.fetchone() is None:
            return False
        else:
            return True

# Thread will be different and hence we have to create a another object of it


def add_admission_features_to_database(email, features):
    conn = sqlite3.connect("AAP.db")
    cursor = conn.cursor()
    featuresStripped = []
    for i in features:
        featuresStripped.append(i.replace(" ", ""))

    lst = json.dumps(featuresStripped)
    query = "update appusers set admission_features=? where email=?"
    result = cursor.execute(query, (lst, email))
    conn.commit()
    if result:
        conn.close()
        return True
    else:
        conn.close()
        return False


def add_placement_features_to_database(email, features):
    conn = sqlite3.connect("AAP.db")
    cursor = conn.cursor()
    featuresStripped = []
    for i in features:
        featuresStripped.append(i.replace(" ", ""))

    lst = json.dumps(featuresStripped)
    query = "update appusers set placement_features=? where email=?"
    result = cursor.execute(query, (lst, email))
    conn.commit()
    if result:
        conn.close()
        return True
    else:
        conn.close()
        return False


def fetch_user_id(email):
    con = sqlite3.connect("AAP.db")
    cursor = con.cursor()
    query = "select id from appusers where email=?"
    result = cursor.execute(query, (email,))
    con.commit()
    id = result.fetchone()[0]
    if id is None:
        con.close()
        return False
    else:
        con.close()
        return id


def fetch_admission_features_from_database(email):
    conn = sqlite3.connect("AAP.db")
    cursor = conn.cursor()
    query = "select admission_features from appusers where email=?"
    result = cursor.execute(query, (email,))
    conn.commit()
    features = json.loads(result.fetchone()[0])
    conn.close()
    return features


def fetch_placement_features_from_database(email):
    conn = sqlite3.connect("AAP.db")
    cursor = conn.cursor()
    query = "select placement_features from appusers where email=?"
    result = cursor.execute(query, (email,))
    conn.commit()
    return json.loads(result.fetchone()[0])


def add_training_mode_admission(mode, email):
    conn = sqlite3.connect("AAP.db")
    cursor = conn.cursor()
    query = "update appusers set Training_Mode_Admission=? where email=?"
    result = cursor.execute(query, (mode, email))
    conn.commit()
    if result:
        conn.close()
        return True
    else:
        conn.close()
        return False


def add_training_mode_placement(mode, email):
    conn = sqlite3.connect("AAP.db")
    cursor = conn.cursor()
    query = "update appusers set Training_Mode_Placement=? where email=?"
    result = cursor.execute(query, (mode, email))
    conn.commit()
    if result:
        conn.close()
        return True
    else:
        conn.close()
        return False


def retrive_training_mode_admission(email):
    '''
    Returns the mode in which admission training has been done
    '''
    con = sqlite3.connect("AAP.db")
    cursor = con.cursor()
    query = "select Training_Mode_Admission from appusers where email=?"
    result = cursor.execute(query, (email,))
    con.commit()
    mode = result.fetchone()[0]
    return mode


def retrive_training_mode_placement(email):
    '''
    Returns the mode in which  placement training has been done
    '''
    con = sqlite3.connect("AAP.db")
    cursor = con.cursor()
    query = "select Training_Mode_Placement from appusers where email=?"
    result = cursor.execute(query, (email,))
    con.commit()
    mode = result.fetchone()[0]
    return mode


def remove_user(email, id):
    try:
        con = sqlite3.connect("AAP.db")
        cursor = con.cursor()
        query = "delete from appusers where email=?"
        result = cursor.execute(query, (email,))
        con.commit()
        con.close()
        os.removedirs(f"Main_Models\\{id}")
    except:
        pass
    return


def AddFeedbacK(name, review):
    name = name.lower()
    '''Add feedback to database'''
    con = sqlite3.connect("Reviews.db")
    cursor = con.cursor()
    query = "create table if not exists reviews(id integer primary key,name text, review text)"
    cursor.execute(query)
    con.commit()

    query = 'select review from reviews where name=?'
    result = cursor.execute(query, (name,))
    con.commit()
    if result.fetchone() is None:
        query = 'insert into reviews(name,review) values(?,?)'
        cursor.execute(query, (name, review))
        con.commit()
    else:
        st.warning("Your review has already been registered")
    con.close()


def FetchFeedback():
    '''Fetch feedback from database'''
    con = sqlite3.connect("Reviews.db")
    cursor = con.cursor()
    query = "create table if not exists reviews(id integer primary key,name text, review text)"
    cursor.execute(query)
    con.commit()

    query = 'select * from reviews'
    result = cursor.execute(query)
    con.commit()
    try:
        id = result.fetchall()
        # name = result.fetchall()[1]
        # review = result.fetchall()[2]
        # st.write(id,name,review)
        con.close()
        return id
    except TypeError as te:
        return None, None, None
