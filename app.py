from flask import Flask, render_template, url_for, request, redirect, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from joblib import load
import random
from string import Template
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField



# Instantiate your models

clf = load("classifier.joblib")


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

global round_num 
global your_score 
global computer_score 
global five_random_piece_index
global i


round_num = 0
your_score = 0
computer_score = 0

five_random_piece_index = []
y_test_length = len(y_test)

i = 0
while i!=5:
    n = random.randint(0,y_test_length-1)
    if n not in five_random_piece_index:
        five_random_piece_index.append(n)
        i = i+1


# Base endpoint to perform prediction.
@app.route('/', methods=['POST', 'GET'])
def play():
    global your_score
    global computer_score
    global round_num

    if round_num == 5:
        if your_score > computer_score:
            winner = "You won!"
        elif your_score < computer_score:
            winner = "Computer won!"
        else:
            winner = "It is a tie!"

        your_final_score = your_score
        computer_final_score = computer_score
        return render_template("end.html", winner = winner, your_final_score = your_final_score, computer_final_score = computer_final_score)

    if request.method == 'POST':
        if request.form['challenge'] == 'YES!' or request.form['challenge'] == 'Ready!':
            piece = "music/" + str(five_random_piece_index[round_num]) + ".m4a"
            return render_template('play.html', your_score =  your_score, computer_score = computer_score, round_num = round_num, piece = piece)
        else:
            return "there was a problem :("

    else:
        return render_template('index.html')

@app.route('/play', methods=['POST', 'GET'])
def user_guess():
    global your_score
    global computer_score
    global round_num


    if request.method == 'POST':
        user_prediction = request.form['user_guess']
        computer_prediction = str(clf.predict(X_test[five_random_piece_index[round_num]].reshape(1,-1))[0])
        correct_composer = y_test[five_random_piece_index[round_num]]
        canonical_title = title_list[five_random_piece_index[round_num]]

        round_num = round_num + 1

        user_prediction_image = user_prediction.split()[-1].lower()+".jpg"
        computer_prediction_image = computer_prediction.split()[-1].lower()+".jpg"
        correct_composer_image = correct_composer.split()[-1].lower()+".jpg"

        only_user_correct = False
        only_computer_correct = False
        both_correct = False
        both_false = False

        if user_prediction == correct_composer and computer_prediction != correct_composer:
            only_user_correct = True
            your_score = your_score + 1
        
        if computer_prediction == correct_composer and user_prediction != correct_composer:
            only_computer_correct = True
            computer_score = computer_score +1 
        
        if user_prediction == correct_composer and computer_prediction == correct_composer:
            both_correct = True
            your_score = your_score + 1
            computer_score = computer_score + 1
        
        if user_prediction != correct_composer and computer_prediction != correct_composer:
            both_false = True
        
        return render_template('results.html', user_prediction = user_prediction, computer_prediction = computer_prediction, correct_composer = correct_composer, user_prediction_image = user_prediction_image, computer_prediction_image = computer_prediction_image, correct_composer_image = correct_composer_image, only_user_correct = only_user_correct, only_computer_correct = only_computer_correct, both_correct = both_correct, both_false = both_false, canonical_title = canonical_title)
    

    else:
        piece = "music/" + str(five_random_piece_index[round_num]) + ".m4a"
        return render_template('play.html', your_score = your_score, computer_score = computer_score, round_num = round_num, piece = piece)

@app.route('/end', methods=['POST', 'GET'])
def play_again():
    global your_score
    global computer_score
    global round_num
    global five_random_piece_index
    global i

    if request.method == 'POST' and request.form['play_again'] == "YES!":
        your_score = 0
        computer_score = 0
        round_num = 0
        five_random_piece_index = []
        i = 0
        while i!=5:
            n = random.randint(0,y_test_length-1)
            if n not in five_random_piece_index:
                five_random_piece_index.append(n)
                i = i+1

        return render_template("index.html")

    else:
        return "Bye!"
    



    

if __name__ == '__main__':
    app.run(debug=True)