#from flask import Flask, render_template, request, session, Session
from flask import *
from joblib import load
import random


#not needed imports
#from flask import url_for, redirect, jsonify, flash
#from datetime import datetime
#from string import Template
#from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField



# Instantiate your models

clf = load("classifier_new.joblib")


# load numpy array from csv file
import numpy as np
from numpy import loadtxt
import pandas as pd
# load array
X_test = loadtxt('X_test.csv', delimiter=',')


df = pd.read_csv('y_test.csv',sep='\t', header=None)
arr = np.array(df)
y_test = arr.flatten()



df = pd.read_csv('titles.csv',sep='\t', header=None)
arr = np.array(df)
title_list = arr.flatten()









app = Flask(__name__)
#SESSION_TYPE = 'filesystem'
#app.config.from_object(__name__)
app.secret_key = "abc"  








# Base endpoint to perform prediction.
@app.route('/', methods=['POST', 'GET'])


def setup():
    y_test_length = len(y_test)
    if request.method == 'POST':
        if request.form['challenge'] == 'YES!':
            session["round_num"] = 0
            session["your_score"] = 0 
            session["computer_score"] = 0
            session["five_random_piece_index"] = []
            session["i"] = 0
            print("initialized")

        while session["i"]!=5:
            n = random.randint(0,y_test_length-1)
            if n not in session["five_random_piece_index"]:
                session["five_random_piece_index"].append(n)
                session["i"] += 1
    
    if request.method == 'POST':
        if (request.form['challenge'] == 'YES!' or request.form['challenge'] == 'Ready!') and session["round_num"] != 5:
            piece = "music/" + str(session["five_random_piece_index"][session["round_num"]]) + ".m4a"
            return render_template('play.html', your_score =  session["your_score"], computer_score = session["computer_score"], round_num = session["round_num"], piece = piece)
        elif session["round_num"] == 5:
            if session["your_score"] > session["computer_score"]:
                winner = "You won!"
            elif session["your_score"] < session["computer_score"]:
                winner = "Computer won!"
            else:
                winner = "It is a tie!"

            your_final_score = session["your_score"]
            computer_final_score = session["computer_score"]
            return render_template("end.html", winner = winner, your_final_score = your_final_score, computer_final_score = computer_final_score)
    else:
        return render_template("index.html")

    
    


def play():

    if session["round_num"] == 5:
        if session["your_score"] > session["computer_score"]:
            winner = "You won!"
        elif session["your_score"] < session["computer_score"]:
            winner = "Computer won!"
        else:
            winner = "It is a tie!"

        your_final_score = session["your_score"]
        computer_final_score = session["computer_score"]
        return render_template("end.html", winner = winner, your_final_score = your_final_score, computer_final_score = computer_final_score)

    if request.method == 'POST':
        if request.form['challenge'] == 'YES!' or request.form['challenge'] == 'Ready!':
            piece = "music/" + str(session["five_random_piece_index"][session["round_num"]]) + ".m4a"
            return render_template('play.html', your_score =  session["your_score"], computer_score = session["computer_score"], round_num = session["round_num"], piece = piece)
    else:
        return render_template("index.html")

    '''
    if request.method == 'POST':
        if request.form['challenge'] == 'YES!' or request.form['challenge'] == 'Ready!':
            piece = "music/" + str(session["five_random_piece_index"][session["round_num"]]) + ".m4a"
            return render_template('play.html', your_score =  session["your_score"], computer_score = session["computer_score"], round_num = session["round_num"], piece = piece)
        else:
            return "there was a problem :("
    else:
        return render_template('index.html')
    '''

@app.route('/play', methods=['POST', 'GET'])
def user_guess():


    if request.method == 'POST':
        user_prediction = request.form['user_guess']
        computer_prediction = str(clf.predict(X_test[session["five_random_piece_index"][session["round_num"]]].reshape(1,-1))[0])
        correct_composer = y_test[session["five_random_piece_index"][session["round_num"]]]
        canonical_title = title_list[session["five_random_piece_index"][session["round_num"]]]

        session["round_num"] = session.get("round_num") + 1

        user_prediction_image = user_prediction.split()[-1].lower()+".jpg"
        computer_prediction_image = computer_prediction.split()[-1].lower()+".jpg"
        correct_composer_image = correct_composer.split()[-1].lower()+".jpg"

        only_user_correct = False
        only_computer_correct = False
        both_correct = False
        both_false = False

        if user_prediction == correct_composer and computer_prediction != correct_composer:
            only_user_correct = True
            session["your_score"] = session["your_score"] + 1
        
        if computer_prediction == correct_composer and user_prediction != correct_composer:
            only_computer_correct = True
            session["computer_score"] = session["computer_score"] +1 
        
        if user_prediction == correct_composer and computer_prediction == correct_composer:
            both_correct = True
            session["your_score"] = session["your_score"] + 1
            session["computer_score"] = session["computer_score"] + 1
        
        if user_prediction != correct_composer and computer_prediction != correct_composer:
            both_false = True
        
        return render_template('results.html', user_prediction = user_prediction, computer_prediction = computer_prediction, correct_composer = correct_composer, user_prediction_image = user_prediction_image, computer_prediction_image = computer_prediction_image, correct_composer_image = correct_composer_image, only_user_correct = only_user_correct, only_computer_correct = only_computer_correct, both_correct = both_correct, both_false = both_false, canonical_title = canonical_title)
    

    #else:
        #piece = "music/" + str(five_random_piece_index[round_num]) + ".m4a"
        #return render_template('play.html', your_score = your_score, computer_score = computer_score, round_num = round_num, piece = piece)

@app.route('/end', methods=['POST', 'GET'])
def play_again():
    y_test_length = len(y_test)
    if request.method == 'POST' and request.form['play_again'] == "YES!":
        session["round_num"]=0
        session["your_score"]=0 
        session["computer_score"]=0 
        session["five_random_piece_index"]=[]
        session["i"]=0
        while session["i"]!=5:
            n = random.randint(0,y_test_length-1)
            if n not in session["five_random_piece_index"]:
                session["five_random_piece_index"].append(n)
                session["i"] = session["i"]+1

        return render_template("index.html")

    #else:
        #return "Bye!"
    


if __name__ == '__main__':
    app.run()
