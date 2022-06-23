import itertools
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import scipy as sp
import os, signals
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
from sklearn.plot_learning_curve import plot_learning_curve
from sklearn.svm import SVC
from sklearn.datasets import load_digits
from sklearn.model_selection import ShuffleSplit
from sklearn.learning_curve import learning_curve


gammas = np.logspace(-6, -1, 10)

if __name__ == '__main__': # entering of main function
	#List of parameters
	SHOW_CONFUSION_MATRIX = True # indicating we don't want to show confusion matrix

	x_data = []  #accelerometer values list
	y_data = [] # target values (class) list

	classes = {} # initialising classes
    
	root="data" #Default directory containing the dataset

	print ("Loading the dataset from '{directory}'...".format(directory=root),)
	#Fetch all the data files from the root directory of the dataset
	for path, subdirs, files in os.walk(root):
		for name in files:
			#Get the filename
			filename = os.path.join(path, name)
			print(filename)
			#Load the sample from file
			sample = signals.Sample.load_from_file(filename)
			print(sample)
			#Linearize the sample and then add it to the x_data list
			x_data.append(sample.get_linearized())
			#Extract the category from the file name
			#For example, the file "a_sample_0.txt" will be considered as "a"
			category = name.split("_")[0]
			number = ord(category) - ord("a")
			#Get a number for the category, as an offset from the category
			#to the a char in Ascii
			if (number >= 0 and number <26):
				y_data.append(number)
			else:
				number=26	
				y_data.append(number)
			#print(number)
			#Add the category to the y_data list
			 #y represents the target class for classification
			#Include the category and the corresponding number into a dictionary
			#for easy access and referencing
			#classes[number] = category
			

	print ("DONE")

	#Parameters used in the cross-validated training process
	#The library automatically tries every possible combination to
	#find the best scoring one.
	params = {'C':[0.001,0.01,0.1,1], 'kernel':['linear']}# C is a regularization parameter, Kernel is linear

	#Inizialize the model
	svc = svm.SVC(probability = True)
	#Inizialize the GridSearchCV with 8 processing cores and maximum verbosity
	clf = GridSearchCV(svc, params,verbose =10, n_jobs=8)

	#Split the dataset into two subset, one used for training and one for testing, 65% training, 35% testing
	X_train, X_test, Y_train, Y_test = train_test_split(x_data, y_data, test_size=0.35, random_state=0)

	print ("Starting the training process...")

	#Start the training process
	clf.fit(X_train, Y_train)
    
   
	#If SHOW_CONFUSION_MATRIX is true, prints the confusion matrix
	if SHOW_CONFUSION_MATRIX:
		print ("Confusion Matrix:")
		Y_predicted = clf.predict(X_test)
		print(classification_report(Y_test,Y_predicted))
  
       # print(confusion_matrix(Y_test, Y_predicted))
       
       

	print ("\nBest estimator parameters: ")
	print (clf.best_estimator_)
	
	#Calculates the score of the best estimator found.
	score = clf.score(X_test, Y_test)
   

  
	print ("\nSCORE: {score}\n".format(score = score))
    
   

	print ("Saving the model...",)

	#Saves the model to the "model.pkl" file
	joblib.dump(clf, 'model.pkl') 
	#Saves the classes to the "classes.pkl" file
	joblib.dump(classes, 'classes.pkl') 
    
	print ("DONE")
    
title = 'Learning Curves (SVM, linear kernel, $\gamma=%.6f$)' 
estimator = SVC(kernel='linear', gamma=clf.best_estimator_.gamma)
plot_learning_curve(estimator, title, X_train, Y_train, cv=cv)
plt.show()    

 




