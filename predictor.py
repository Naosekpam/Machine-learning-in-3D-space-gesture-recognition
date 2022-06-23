import serial
import time
import sys
from sklearn import svm
import scipy as sp
import os, signals
from sklearn.externals import joblib
from pynput.keyboard import Key,Controller
keyboard = Controller()


def remove_myfile(): # function to remove  file
    folder = 'C:\\Users\\veronica\\project\\predict\\'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print("error while removing"+str(e))
print("Start")
port="COM8" #This will be different for various devices and on windows it will probably be a COM port.
bluetooth=serial.Serial(port, 9600)#Start communications with the bluetooth unit
print("Connected")

bluetooth.flushInput() #This gives the bluetooth a little kick
bluetooth.write(b"BOOP ") #Bluetooth cannot continuously streamed the data, need to ping it at time to time
clf = joblib.load('model.pkl')
for i in range(0,30):
    print(i)
    data = open("C:\\Users\\veronica\\project\\predict\\output.txt","w") #Change the file path (make a folder called data)
    if i== 30:
        for char in "Work\n\n":
            keyboard.press(char)
            keyboard.release(char)

    while True: #send 6 groups of data to the bluetooth
        bluetooth.write(b"BOOP")
		#print(i)
		#print("Ping")
		#bluetooth.write(b"BOOP "+str.encode(str(i)))#These need to be bytes not unicode, plus a number
        input_data=bluetooth.readline()#This reads the incoming data. In this particular example it will be the "Hello from Blue" line
		#print(input_data.decode())#These are bytes coming in so a decode is needed
        Status= input_data.decode()
		#print(repr(Status).rstrip())
		#print(repr("S"))
        if Status =="C\r\n":
			
            data.close()
            bluetooth.flushInput() #clearning the buffer
            bluetooth.flushOutput()
            x_data = []
            root="predict" #Default directory containing the dataset
            print ("Loading the dataset from '{directory}'...".format(directory=root),)
            for path, subdirs, files in os.walk(root):
                for name in files:
                        #Get the filename
                        filename = os.path.join(path, name)
                        print(filename)
                        #Load the sample from file
                        sample = signals.Sample.load_from_file(filename)
                        #Linearize the sample and then add it to the x_data list
                        x_data.append(sample.get_linearized())
                        #Extract the category from the file name
                        #For example, the file "a_sample_0.txt" will be considered as "a"
            print ("DONE")
            print(x_data)
            number = clf.predict(x_data)
            print(number)

            if number==0:
                keyboard.press('a')
                keyboard.release('a')
            if number==1:
                keyboard.press('b')
                keyboard.release('b')
            if number==2:
                keyboard.press('c')
                keyboard.release('c')
            if number==3:
                keyboard.press('d')
                keyboard.release('d')
            if number==4:
                keyboard.press('e')
                keyboard.release('e')
            if number==5:
                keyboard.press('f')
                keyboard.release('f')
            if number==6:
                keyboard.press('g')
                keyboard.release('g')
            if number==7:
                keyboard.press('h')
                keyboard.release('h')
            if number==8:
                keyboard.press('i')
                keyboard.release('i')
            if number==9:
                keyboard.press('j')
                keyboard.release('j')
            if number==10:
                keyboard.press('k')
                keyboard.release('k')
            if number==11:
                keyboard.press('l')
                keyboard.release('l')
            if number==12:
                keyboard.press('m')
                keyboard.release('m')
            if number==13:
                keyboard.press('n')
                keyboard.release('n')
            if number==14:
                keyboard.press('o')
                keyboard.release('o')
            if number==15:
                keyboard.press('p')
                keyboard.release('p')
            if number==16:
                keyboard.press('q')
                keyboard.release('q')
            if number==17:
                keyboard.press('r')
                keyboard.release('r')
            if number==18:
                keyboard.press('s')
                keyboard.release('s')
            if number==19:
                keyboard.press('t')
                keyboard.release('t')
            if number==20:
                keyboard.press('u')
                keyboard.release('u')
            if number==21:
                keyboard.press('v')
                keyboard.release('v')
            if number==22:
                keyboard.press('w')
                keyboard.release('w')
            if number==23:
                keyboard.press('x')
                keyboard.release('x')
            if number==24:
                keyboard.press('y')
                keyboard.release('y')    
            if number==25:
                keyboard.press('z')
                keyboard.release('z')  
            if number==26:
                keyboard.press(' ')
                keyboard.release(' ')  
            remove_myfile
            break
        Value_list=[]
        while Status == "S\r\n":
            print("entering")
            input_data=bluetooth.readline()
            Value= input_data.decode()   #This reads the incoming data. In this particular example it will be the "Hello from Blue" line
            if Value=="E\r\n":
                Value_list=[]
                print("breaking")
                break
            else:
                Value_list.append(Value.rstrip())
                if(len(Value_list)>5):
                    print(Value_list)
                    row = (Value_list)
                    data.write("START"+" "+str(row[0])+" "+ str(row[1])+" "+str(row[2])+" "+str(row[3])+" "+str(row[4])+" "+str(row[5])+" "+ "END"+"\n")
bluetooth.close() #Otherwise the connection will remain open until a timeout which ties up the /dev/thingamabob
print("Done")