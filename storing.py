import serial
import time
import sys

print("Start")
port="COM8" #This will be different for various devices and on windows it will probably be a COM port.
bluetooth=serial.Serial(port, 9600)#Start communications with the bluetooth unit
print("Connected")
bluetooth.flushInput() #This gives the bluetooth a little kick
bluetooth.write(b"BOOP ") #sending boop to arduino just to check connection
for i in range(0,20): # number of instance that i want to record
	print(i)
	data = open("C:\\Users\\veronica\\project\\data\\g_sample_0_"+str(i)+".txt","w") #Change the file path (make a folder called data)
	while True: #send 6 groups of data to the bluetooth
		bluetooth.write(b"BOOP")# arduino in bluetooth can't continiously send data so we need to contiously ping the bluetooth.
		input_data=bluetooth.readline()#This reads the incoming data. It will read the acelerometer value and any data send from bluetooth
		Status= input_data.decode()# decoding the incoming data because arduino sends data encoded using utf-8
		if Status =="C\r\n": #indication send from the arduino to close the file
			data.close() # closing the file
			bluetooth.flushInput() #flushing bluetooth input and output
			bluetooth.flushOutput()
			break #breaking from first while
		Value_list=[] #initializing an empty list to store the data
		
		while Status == "S\r\n": # if status is "S" we know that data have started to come
			print("entering")
			input_data=bluetooth.readline()# reading accelerometer valaues
			Value= input_data.decode()   #This reads the incoming data. In this particular example it will be the "Hello from Blue" line
			if Value=="E\r\n":# if its E one instance is complete
				Value_list=[] # reinitializing an empty array
				print("breaking")
				break# breaking from 2nd while
			else:
				Value_list.append(Value.rstrip()) # we are appending the values read in the list
				if(len(Value_list)>5): # when the list size is 5 enter
					print(Value_list)
					row = (Value_list) #assigning list to a row
					data.write("START"+" "+str(row[0])+" "+ str(row[1])+" "+str(row[2])+" "+str(row[3])+" "+str(row[4])+" "+str(row[5])+" "+ "END"+"\n") 
					
	
			


	
bluetooth.close() #Otherwise the connection will remain open until a timeout which ties up the /dev/thingamabob
print("Done")

