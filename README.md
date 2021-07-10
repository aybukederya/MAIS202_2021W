# MAIS202_2021W
2021 Winter MAIS 202 Final Project

MAIS 202 is a bootcamp offered by McGill Artificial Intelligence Society. It is an intensive, ten-week long accelerated introduction to machine learning. "Guessthecomposer" is my final project of the MAIS 202. 

"Guessthecomposer" is a game in which the user competes with the machine learning model to identify the composers of the newly heard pieces. The model is a random forest multiclass classifier, and it was trained on hundreds of pieces by Bach, Beethoven, Chopin, Liszt and Schubert, found in the Maestro Dataset. The model predicts the composer of the newly heard song, based on its numerous musical attributes and how they relate to the pieces of the same composers the computer was trained on. The model has 77% accuracy on the validation set.

To try your musical knowledge, please check out my deployed web-app: https://guessthecomposer.herokuapp.com/


Alternatively, you can run the web-app locally. First install all packages in requirements.txt. Then, type "python app.py" to run the flask app. Open a browser and navigate to your http://localhost:5000.


Maestro Dataset:

Curtis Hawthorne, Andriy Stasyuk, Adam Roberts, Ian Simon, Cheng-Zhi Anna Huang, Sander Dieleman, Erich Elsen, Jesse Engel, and Douglas Eck. "Enabling Factorized Piano Music Modeling and Generation with the MAESTRO Dataset." In International Conference on Learning Representations, 2019.

