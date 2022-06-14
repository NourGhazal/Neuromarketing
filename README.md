# Neuromarketing
This repository contains the work of my bachelor project and how the project was gradually built.\
The data used in this project was not included in the repo for privacy reasons.\
The Jupyter notebooks in the repo show the progress done when optimizing data.\
The final product is in the python file interface.py and the life testing version is life_test.py.\
The idea of the project is as follows :
- Collect EEG signals from the participants while they are viewing posters for marketing campaigns.
- Each image lasts for 4 seconds 
- After each image the participants is required to specify if he liked/disliked the image using 1:5 scale and the collected data is labelled accordingly 
- if the subject selected Neutral the data for the image is discarded 
- After finishing the previous phase which is called training phase the data is filtered and a Random forest model is trained on the data and its labeled the it is saved in the trees folder with the name of the subject as a .pkl object 
- After Training the model the participant could start the live testing phase
- During the live testing phase an image is displayed to the user and EEG data is collected. The data is then filtered using the same approach as before and the then givin to the trained model to determine whether the user liked the image or not in real time.
# Research Paper Reference:
https://link.springer.com/article/10.1007/s11042-017-4580-6
# Thesis on the project:
https://drive.google.com/file/d/1kSO6sLyWEO91wJSP7xxPPvlq7-q_sYug/view?usp=sharing
  
