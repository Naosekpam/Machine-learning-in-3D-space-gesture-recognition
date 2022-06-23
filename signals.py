import numpy as np
from sklearn.preprocessing import scale
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

class Sample:
	'''
	Sample is used to load, store and process the signals obtained 
	from the accelerometers.
	It provides a method to load the signals from file and process them.
	'''
	def __init__(self, acx, acy, acz, gx, gy, gz):
		self.acx = acx
		self.acy = acy
		self.acz = acz
		self.gx = gx
		self.gy = gy
		self.gz = gz

	def get_linearized(self, reshape = False):
		'''
		Linearize the data, combining the 6 different axes.
		Useful to feed the data into a machine learning algorithm.

		If reshape=True it reshape it (Useful when feeding it to the predict method)
		'''
		if reshape:
			return np.concatenate((self.acx, self.acy, self.acz, self.gx, self.gy, self.gz)).reshape(1,-1)
		else:
			return np.concatenate((self.acx, self.acy, self.acz, self.gx, self.gy, self.gz))
		

	@staticmethod
	def load_from_file(filename, size_fit = 50):
		'''
		Loads the signal data from a file.
		
		filename: indicates the path of the file.
		
		size_fit: is the final number of sample an axe will have.
				  It uses linear interpolation to increase or decrease
				  the number of samples.

		'''
		#Load the signal data from the file as a list
		#It skips the first and the last line and converts each number into an int
		data_raw=[]
		
		for i in open(filename) :
			data_raw.append(list(map(lambda x: int(x), i.split(" ")[1:-1]))) # removing first and last and splitting by " "
			
			
        
	#	print(data_raw) #appends the data from all files as a list  
		#Convert the data into floats
		data = np.array(data_raw).astype(float) #convert the data as a floas value. An it is saved as array for files of each letter.
		print(data.shape) #gives the shape of an array (raw,column)

		#Standardize the data by scaling it
		data_norm=scale(data)
	    
		#Extract each axe into a separate variable
		#These rapresent the acceleration in the 3 axes
	    
		acx = data_norm[:,0]
		acy = data_norm[:,1]
		acz = data_norm[:,2]
		

		#These rapresent the rotation in the 3 axes
		gx = data_norm[:,3]
		gy = data_norm[:,4]
		gz = data_norm[:,5]
		

		#Create a function for each axe that interpolates the samples
		x = np.linspace(0, data.shape[0], data.shape[0]) # generate evenly space number for each row of the array
		#like for row from 0 to 30, take out the data, data.shape[0] -> row no.
		#Return evenly spaced numbers over a specified interval.
        #Returns num evenly spaced samples, calculated over the interval [start, stop].
        #The endpoint of the interval can optionally be excluded.
		print("Data result after linespace")
		print(x)
		print(x.shape)
		#feature extraction
		f_acx = interp1d(x, acx)
		
		f_acy = interp1d(x, acy)
		f_acz = interp1d(x, acz)

		f_gx = interp1d(x, gx)
		f_gy = interp1d(x, gy)
		f_gz = interp1d(x, gz)

		#Create a new sample set with the desired sample size by rescaling
		#the original one
		xnew = np.linspace(0, data.shape[0], size_fit)
		print("Xnew")
		print(xnew)
		acx_stretch = f_acx(xnew)
		acy_stretch = f_acy(xnew)
		acz_stretch = f_acz(xnew)

		gx_stretch = f_gx(xnew)
		gy_stretch = f_gy(xnew)
		gz_stretch = f_gz(xnew)

		#Returns a Sample with the calculated values
		return Sample(acx_stretch, acy_stretch, acz_stretch, gx_stretch, gy_stretch, gz_stretch)
	  