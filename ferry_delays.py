#first attempt at python programming, file access, analysis
# based on seng265 assignment
import os
import sys
import inspect
from datetime import datetime

# included from https://stackoverflow.com/questions/6810999/how-to-determine-file-function-and-line-number/6811020
# implements __LINE__ functionality for debugging, as in c++
# requires import sys
class __LINE__(object):
    def __repr__(self):
        try:
            raise Exception
        except:
            return str(sys.exc_info()[2].tb_frame.f_back.f_lineno)

__LINE__ = __LINE__()
# END line functionality

# month = 2 #january
port_names = {'t':'Tsawwassen','s':'Schwartz Bay'}
month_array = ["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
file_list = []
delay = 0
count = 0
headers = []
cur_line = {}

def check_filenames():
	# print (sys.argv)
	if len(sys.argv) == 1:
		print ('no file names supplied, line {}. Exiting...'.format(__LINE__))
		exit(1)

	for name in sys.argv[1:]:
		# array indices start at 0 !!!
		# just exclude the first argument since its the script name
		try:
			f = open(name)
			f.close()
			file_list.append(name) #append is ok, does not alter reference
		except:
			print("couldn't open file {}. Exiting...".format(name))
			exit(1)
	

def calc_avg_delay(dep,month):
	# recieves a departure terminal and a month
	# will be aware of file names to scan based on sys.argv
	# assumes file names are OK and can be opened
	# returns the avg_delay in minutes

	# print("delay func called with arguments dep = {} and month = {}".format(dep,month))
	delay = 0
	count = 0
	# print (file_list)
	for name in file_list:
		# print("line {}, opening file {} ... ".format(__LINE__,name))
		f = open(name)
		# print("file opened: {}".format(name))
		headers = f.readline().split(",") # redundant but will accomodate various files which have different col orders
		# print(headers)
		# print ("in file {} for month number {}, listing as following:".format(name,month))
		#format scheduled and actual departure time, but only if month is corresponding to requested month
		for line in f:
			cur_line = dict(zip(headers,line.split(","))) 
			#the zip method combines headers with corresponding values. not clean, but makes for much more readable code
			if int(cur_line["scheduled_departure_month"]) == month and cur_line["departure_terminal"] == dep:
				# difference calculation algorithm
				if cur_line["actual_departure_hour"] >= cur_line["scheduled_departure_hour"]:
					#resolve hours if necessary, then substract minutes, the difference sign will align as necessary
					diff = 60*(int(cur_line["actual_departure_hour"]) - int(cur_line["scheduled_departure_hour"])) + int(cur_line["actual_departure_minute"]) - int(cur_line["scheduled_departure_minute"]) 
				else:
					# basically flip, and assign neg sign
					diff = -(60*(int(cur_line["scheduled_departure_hour"]) - int(cur_line["actual_departure_hour"])) + int(cur_line["scheduled_departure_minute"]) - int(cur_line["actual_departure_minute"])) 
	
					#for debugging --
				scheduled_departure_time = cur_line["scheduled_departure_hour"] + ":" + cur_line["scheduled_departure_minute"]
				actual_departure_time = cur_line["actual_departure_hour"] + ":" + cur_line["actual_departure_minute"]
					
				delay += diff # delay will count up in minutes
				count += 1

				# print ("scheduled: {}, actual: {}, delay in minutes: {}".format(scheduled_departure_time, actual_departure_time, diff))
		f.close()

	if count > 0:
		return {"entries": count, "delay":float(delay/count)}
	else:
		return {"entries": 0, "delay": 0}

def menu():
	print ("""
	Average ferry delay calculator, by arkadi, 20171216'
	This program accepts pre-formatted bc ferry schedule csv files between Tswwassen and Schwartz Bay, and calculates the
	average sailing delay based on month and departure terminal

	to use, make a selection of point of departure (t or s) and the number of month (1-12)
	To quit, enter 'q' at any point
	""")

	month = ''
	dep = ''

	while dep != 'q':
		month = input("Enter month (1-12):")

		dep = input("Enter departure terminal (t or s):")
	
		#error checking
		if dep == 't' or dep == 's':
			try:
				int_month = int(month)
			except:
				print("non numerical month entered.")
				continue

			if int_month >=1 and int_month <=12:
				# do the calculation
				res = calc_avg_delay(port_names[dep],int_month)
				# print("hi")
				# print(calc_avg_delay(port_names[dep],int_month))
				print ("RESULTS\n\tfor the month of {}, based on {} entries in {} files, the average delay departing from {} terminal was {:.2f} minutes.\nEND RESULTS".format(month_array[int_month],res["entries"], len(file_list),port_names[dep],res["delay"]))


			else:
				print ("incorrect month entered: {}".format(int_month))
			
		else:
			print ("incorrect departure terminal entered")
		
		# month = input("Enter month (1-12):")
		# dep = input("Enter departure terminal (t or s):")

def main():
	
	# read file arguments, prompt if errors
	check_filenames()
	print("from main, printing file list: {}".format(file_list))
	#init menu, read responses
	menu()

if __name__ == "__main__":
	main()
